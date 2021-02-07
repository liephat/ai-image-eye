import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Label from './ui/Label';
import { flaskUrl } from './constants';

class ImageThumbnail extends React.Component {
    constructor(props) {
        super(props);
        this.labelKey = this.labelKey.bind(this);
    }

    labelKey(label) {
        return this.props.name + label.name;
    }

    render() {
        return (
            <Figure>
                <Figure.Image
                    src={flaskUrl(this.props.thumbnail_url)}
                    />
                <Figure.Caption className="text-center">
                    <span className="title">{this.props.name}</span><br/>
                    {this.props.labels.map((label) => {
                        return (<Label label={label} key={this.labelKey(label)} />);
                    })}
                </Figure.Caption>
            </Figure>
        );
    }
}

export default ImageThumbnail;