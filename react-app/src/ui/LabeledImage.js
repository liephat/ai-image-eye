import React from 'react';
import Figure from 'react-bootstrap/Figure';

class LabeledImage extends React.Component {
    constructor(props) {
        super(props);
        this._renderBox = this._renderBox.bind(this);
        this.url = props.url;
        this.labelAssignments = props.labelAssignments;
        this.state = {
            highlightedLabelId: null,
        };
    }

    _renderBox(la) {
        if (la.box) {
            let style = {
                top: la.box.top + '%',
                left: la.box.left + '%',
                bottom: la.box.bottom + '%',
                right: la.box.right + '%',
            };
            return (<div class='label-box' style={style}>
                <div class='label-name'>{la.label.name}</div>
            </div>);
        }
        return (<></>);
    }

    render() {
        let image = (<Figure.Image
            src={this.url}
        />);
        let laId = this.state.highlightedLabelId;
        let overlay = (<></>);

        if (laId || true) {
            overlay = this.labelAssignments.map((la) => {
                if (la.label_assignment_id === laId || true) {
                    return this._renderBox(la);
                }
                return (<></>);
            });
        }

        return (<div class='image-label-parent'>{image}{overlay}</div>);
    }
}

export default LabeledImage;