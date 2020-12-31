import React from 'react';
import ImageThumbnail from './ImageThumbnail';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

class Gallery extends React.Component {
    state = {
        images: [],
        numLoaded: 3,
    }

    constructor(props) {
        super(props);
        this.loadMore = this.loadMore.bind(this);
    }

    componentDidMount() {
        fetch('/all_images').then(res => res.json()).then(data => {
            console.log(data)
            this.setState({
                images: data.images
            });
        });
    }

    loadMore() {
        let numLoadMore = this.state.numLoaded + 3
        this.setState({
            numLoaded: numLoadMore,
        })
    }

    render() {
        return (
        <>
            <Row>
                {this.state.images.slice(0, this.state.numLoaded).map((image, i) => {
                    return (<ImageThumbnail key={image.uid} path={image.path} />)
                })}
            </Row>
            <Row className="justify-content-center">
                <Col xs="auto">
                    <Button onClick={this.loadMore}>Load more ({this.state.numLoaded}/{this.state.images.length})</Button>
                </Col>
            </Row>
        </>
        );
    }
}

export default Gallery;
