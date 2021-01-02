import React from 'react';
import Figure from 'react-bootstrap/Figure';
import Col from 'react-bootstrap/Col';

class ImageThumbnail extends React.Component {
    render() {
        return (
            <Col md={4}>
                <Figure>
                    <Figure.Image
                        src={this.props.path}
                     />
                    <Figure.Caption>
                        {this.props.path}
                    </Figure.Caption>
                </Figure>
            </Col>
        );
    }
}

export default ImageThumbnail;