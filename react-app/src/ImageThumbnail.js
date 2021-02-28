import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Label from './ui/Label';
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
                <Figure.Image
                    src={flaskUrl(this.props.thumbnail_url)}
                    />
                <Figure.Caption className="text-center">
                    <span className="title">{this.props.name}</span><br/>
                    {this.props.label_assignments.map((la) => {
                        return (<Label label={la.label} key={this.labelKey(la)} />);
                    })}
                </Figure.Caption>
            </Figure>
        );
    }
}

export default ImageThumbnail;