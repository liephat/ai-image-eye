import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Label from './ui/Label';
import LabeledImage from './ui/LabeledImage';
import { flaskUrl } from './constants';

class ImageThumbnail extends React.Component {
    constructor(props) {
        super(props);
        this.labelKey = this.labelKey.bind(this);
        this.startHighlight = this.startHighlight.bind(this);
        this.endHighlight = this.endHighlight.bind(this);
        this.state ={
            highlightedLabelAssignmentId: null
        };
    }

    labelKey(label_assignment) {
        return this.props.name + '__' + label_assignment.label_assignment_id;
    }

    /**
     * Called from Label component when the mouse enters it.
     *
     * @param {*} label_assignment LabelAssignment that is to be highlighted
     */
    startHighlight(label_assignment) {
        this.setState({
            highlightedLabelAssignmentId: label_assignment.label_assignment_id
        });
    }

    /**
     * Called from Label component when the mouse leaves it.
     *
     * @param {*} label_assignment LabelAssignment that is to be un-highlighted
     */
    endHighlight(label_assignment) {
        this.setState({
            highlightedLabelAssignmentId: null
        });
    }

    render() {


        let labeled_image = (<LabeledImage
            url={flaskUrl(this.props.thumbnail_url)} labelAssignments={this.props.label_assignments}
            full_image_url={flaskUrl(this.props.url)}
            highlightedLabelAssignmentId={this.state.highlightedLabelAssignmentId} />
        );
        return (
            <Figure>
                {labeled_image}
                <Figure.Caption className="text-center">
                    <span className="title">{this.props.name}</span><br/>
                    {this.props.label_assignments.map((la) => {
                        return (<Label label_assignment={la}
                            key={this.labelKey(la)}
                            startHighlight={this.startHighlight}
                            endHighlight={this.endHighlight}
                            />);
                    })}
                </Figure.Caption>
            </Figure>
        );
    }
}

export default ImageThumbnail;