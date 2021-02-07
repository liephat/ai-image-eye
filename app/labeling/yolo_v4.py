import colorsys
import os

import cv2
import numpy as np
import random

from scipy import special

from app.labeling.model import Model
from app.config.parser import ConfigParser


class YoloV4(Model):

    _anchors = None
    _strides = [8, 16, 32]
    _xy_scale = np.array([1.2, 1.1, 1.05])

    def __init__(self, model, labels, input_size=416):
        super().__init__(model, labels)

        config = ConfigParser()

        if self._anchors is None:
            self._anchors = self.get_anchors(config.anchors_file('yolov4'))

        self.input_size = input_size

    def classify(self, image):

        # preprocessing incoming image
        original_image = cv2.imread(image)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # get the name of the first input of the labeling
        input_name = self.session.get_inputs()[0].name

        # get the output names
        outputs = self.session.get_outputs()
        output_names = [output.name for output in outputs]  # list(map(lambda output: output.name, outputs))

        # set preprocessed image as input and compute predictions
        input_data = self._preprocess(np.copy(original_image), self.input_size)
        raw_result = self.session.run(output_names, {input_name: input_data})

        # post process raw result, result: [x_min, y_min, x_max, y_max, probability, cls_id] format coordinates.
        result = self._postprocess(raw_result, original_image)

        labels = []
        bounding_boxes = []
        confidences = []
        for _, bbox in enumerate(result):
            coor = np.array(bbox[:4], dtype=np.int32)
            c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])

            labels += self.labels(int(bbox[5]))
            confidences += bbox[4]
            bounding_boxes += (c1, c2)

        return labels, confidences, bounding_boxes

    @staticmethod
    def _preprocess(image, input_size):
        ih, iw = [input_size, input_size]
        h, w, _ = image.shape

        scale = min(iw / w, ih / h)
        nw, nh = int(scale * w), int(scale * h)
        image_resized = cv2.resize(image, (nw, nh))

        image_padded = np.full(shape=[ih, iw, 3], fill_value=128.0)
        dw, dh = (iw - nw) // 2, (ih - nh) // 2
        image_padded[dh:nh + dh, dw:nw + dw, :] = image_resized
        image_padded = image_padded / 255.

        image_data = image_padded[np.newaxis, ...].astype(np.float32)

        return image_data

    def _postprocess(self, raw_result, original_image):
        original_image_size = original_image.shape[:2]

        pred_bbox = self._postprocess_bbbox(raw_result)
        bboxes = self._postprocess_boxes(pred_bbox, original_image_size, self.input_size, 0.25)
        bboxes = self._nms(bboxes, 0.213, method='nms')

        return bboxes

    def _postprocess_bbbox(self, pred_bbox):
        """
        Define anchor boxes
        """

        for i, pred in enumerate(pred_bbox):
            conv_shape = pred.shape
            output_size = conv_shape[1]
            conv_raw_dxdy = pred[:, :, :, :, 0:2]
            conv_raw_dwdh = pred[:, :, :, :, 2:4]
            xy_grid = np.meshgrid(np.arange(output_size), np.arange(output_size))
            xy_grid = np.expand_dims(np.stack(xy_grid, axis=-1), axis=2)

            xy_grid = np.tile(np.expand_dims(xy_grid, axis=0), [1, 1, 1, 3, 1])
            xy_grid = xy_grid.astype(np.float)

            pred_xy = ((special.expit(conv_raw_dxdy) * self._xy_scale[i]) - 0.5 * (self._xy_scale[i] - 1) + xy_grid) * self._strides[i]
            pred_wh = (np.exp(conv_raw_dwdh) * self._anchors[i])
            pred[:, :, :, :, 0:4] = np.concatenate([pred_xy, pred_wh], axis=-1)

        pred_bbox = [np.reshape(x, (-1, np.shape(x)[-1])) for x in pred_bbox]
        pred_bbox = np.concatenate(pred_bbox, axis=0)
        return pred_bbox

    @staticmethod
    def _postprocess_boxes(pred_bbox, org_img_shape, input_size, score_threshold):
        """
        Remove boundary boxs with a low detection probability
        """
        valid_scale = [0, np.inf]
        pred_bbox = np.array(pred_bbox)

        pred_xywh = pred_bbox[:, 0:4]
        pred_conf = pred_bbox[:, 4]
        pred_prob = pred_bbox[:, 5:]

        # # (1) (x, y, w, h) --> (xmin, ymin, xmax, ymax)
        pred_coor = np.concatenate([pred_xywh[:, :2] - pred_xywh[:, 2:] * 0.5,
                                    pred_xywh[:, :2] + pred_xywh[:, 2:] * 0.5], axis=-1)
        # # (2) (xmin, ymin, xmax, ymax) -> (xmin_org, ymin_org, xmax_org, ymax_org)
        org_h, org_w = org_img_shape
        resize_ratio = min(input_size / org_w, input_size / org_h)

        dw = (input_size - resize_ratio * org_w) / 2
        dh = (input_size - resize_ratio * org_h) / 2

        pred_coor[:, 0::2] = 1.0 * (pred_coor[:, 0::2] - dw) / resize_ratio
        pred_coor[:, 1::2] = 1.0 * (pred_coor[:, 1::2] - dh) / resize_ratio

        # # (3) clip some boxes that are out of range
        pred_coor = np.concatenate([np.maximum(pred_coor[:, :2], [0, 0]),
                                    np.minimum(pred_coor[:, 2:], [org_w - 1, org_h - 1])], axis=-1)
        invalid_mask = np.logical_or((pred_coor[:, 0] > pred_coor[:, 2]), (pred_coor[:, 1] > pred_coor[:, 3]))
        pred_coor[invalid_mask] = 0

        # # (4) discard some invalid boxes
        bboxes_scale = np.sqrt(np.multiply.reduce(pred_coor[:, 2:4] - pred_coor[:, 0:2], axis=-1))
        scale_mask = np.logical_and((valid_scale[0] < bboxes_scale), (bboxes_scale < valid_scale[1]))

        # # (5) discard some boxes with low scores
        classes = np.argmax(pred_prob, axis=-1)
        scores = pred_conf * pred_prob[np.arange(len(pred_coor)), classes]
        score_mask = scores > score_threshold
        mask = np.logical_and(scale_mask, score_mask)
        coors, scores, classes = pred_coor[mask], scores[mask], classes[mask]

        return np.concatenate([coors, scores[:, np.newaxis], classes[:, np.newaxis]], axis=-1)

    @staticmethod
    def _bboxes_iou(boxes1, boxes2):
        """
        Calculate the Intersection Over Union value
        """
        boxes1 = np.array(boxes1)
        boxes2 = np.array(boxes2)

        boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (boxes1[..., 3] - boxes1[..., 1])
        boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (boxes2[..., 3] - boxes2[..., 1])

        left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
        right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

        inter_section = np.maximum(right_down - left_up, 0.0)
        inter_area = inter_section[..., 0] * inter_section[..., 1]
        union_area = boxes1_area + boxes2_area - inter_area
        ious = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)

        return ious

    @staticmethod
    def _nms(bboxes, iou_threshold, sigma=0.3, method='nms'):
        """
        :param bboxes: (xmin, ymin, xmax, ymax, score, class)

        Note: soft-nms, https://arxiv.org/pdf/1704.04503.pdf
              https://github.com/bharatsingh430/soft-nms
        """
        labels_in_image = list(set(bboxes[:, 5]))
        best_bboxes = []

        for label in labels_in_image:
            label_mask = (bboxes[:, 5] == label)
            label_bboxes = bboxes[label_mask]

            while len(label_bboxes) > 0:
                max_ind = np.argmax(label_bboxes[:, 4])
                best_bbox = label_bboxes[max_ind]
                best_bboxes.append(best_bbox)
                label_bboxes = np.concatenate([label_bboxes[: max_ind], label_bboxes[max_ind + 1:]])
                iou = YoloV4._bboxes_iou(best_bbox[np.newaxis, :4], label_bboxes[:, :4])
                weight = np.ones((len(iou),), dtype=np.float32)

                assert method in ['nms', 'soft-nms']

                if method == 'nms':
                    iou_mask = iou > iou_threshold
                    weight[iou_mask] = 0.0

                if method == 'soft-nms':
                    weight = np.exp(-(1.0 * iou ** 2 / sigma))

                label_bboxes[:, 4] = label_bboxes[:, 4] * weight
                score_mask = label_bboxes[:, 4] > 0.
                label_bboxes = label_bboxes[score_mask]

        return best_bboxes

    @staticmethod
    def draw_bbox(image, bboxes, labels, show_label=True):
        """
        bboxes: [x_min, y_min, x_max, y_max, probability, cls_id] format coordinates.
        """

        num_classes = len(labels)
        image_h, image_w, _ = image.shape
        hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

        random.seed(0)
        random.shuffle(colors)
        random.seed(None)

        for _, bbox in enumerate(bboxes):
            coor = np.array(bbox[:4], dtype=np.int32)
            font_scale = 0.5
            score = bbox[4]
            label_ind = int(bbox[5])
            bbox_color = colors[label_ind]
            bbox_thick = int(0.6 * (image_h + image_w) / 600)
            c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
            cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

            if show_label:
                bbox_mess = '%s: %.2f' % (labels[label_ind], score)
                t_size = cv2.getTextSize(bbox_mess, 0, font_scale, thickness=bbox_thick // 2)[0]
                cv2.rectangle(image, c1, (c1[0] + t_size[0], c1[1] - t_size[1] - 3), bbox_color, -1)
                cv2.putText(image, bbox_mess, (c1[0], c1[1] - 2), cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)

        return image

    @staticmethod
    def get_anchors(anchors_path):
        """
        Loads the anchors from a file.
        """
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = np.array(anchors.split(','), dtype=np.float32)
        return anchors.reshape(3, 3, 2)
