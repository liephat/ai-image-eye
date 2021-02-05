import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Label from './ui/Label';

class ImageThumbnail extends React.Component {
    render() {
        return (
            <Figure>
                <Figure.Image
                    src={this.props.thumbnail_url}
                    />
                <Figure.Caption>
                    <span class="title">{this.props.name}</span><br/>
                    {this.props.labels.map((label) => {
                        return (<Label label={label} />);
                    })}
                </Figure.Caption>
            </Figure>
        );
    }
}

export default ImageThumbnail;