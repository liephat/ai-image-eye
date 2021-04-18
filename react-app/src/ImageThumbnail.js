import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Label from './ui/Label';
import LabeledImage from './ui/LabeledImage';
import { flaskUrl } from './constants';

class ImageThumbnail extends React.Component {
    constructor(props) {
        super(props);
        this.labelKey = this.labelKey.bind(this);
    }

    labelKey(label_assignment) {
        return this.props.name + '__' + label_assignment.label_assignment_id;
    }

    render() {
        return (
            <Figure>
                <LabeledImage url={flaskUrl(this.props.thumbnail_url)} labelAssignments={this.props.label_assignments} />
                <Figure.Caption className="text-center">
                    <span className="title">{this.props.name}</span><br/>
                    {this.props.label_assignments.map((la) => {
                        return (<Label label_assignment={la} key={this.labelKey(la)} />);
                    })}
                </Figure.Caption>
            </Figure>
        );
    }
}

export default ImageThumbnail;