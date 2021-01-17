import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Col from 'react-bootstrap/Col';
import Label from './ui/Label';

class ImageThumbnail extends React.Component {
    render() {
        return (
            <Col md={4}>
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
            </Col>
        );
    }
}

export default ImageThumbnail;