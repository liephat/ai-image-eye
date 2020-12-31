import React from 'react';
import ImageThumbnail from './ImageThumbnail';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

class Gallery extends React.Component {

    constructor(props) {
        super(props);
        this._loadMore = this._loadMore.bind(this);
        this.state = {
            images: [],
            numLoaded: 0,
        }
    }

    componentDidMount() {
        fetch('/all_images').then(res => res.json()).then(data => {
            console.log(data)
            this.setState({
                images: data.images,
                numLoaded: 6,
            });
        });
        this._installScrollObserver();
    }

    _installScrollObserver() {
        var options = {
            root: null,
            rootMargin: "0px",
            threshold: 1.0
        };

        this.observer = new IntersectionObserver(
            this._loadMore,
            options
        );
        this.observer.observe(this.loadingRef);
    }

    _loadMore() {
        let numLoadMore = Math.min(this.state.numLoaded + 3, this.state.images.length);
        this.setState({
            numLoaded: numLoadMore,
        })
    }

    render() {
        const loadingCss = {
            height: "100px",
            margin: "30px",
        }
        return (
        <>
            <Row>
                {this.state.images.slice(0, this.state.numLoaded).map((image, i) => {
                    return (<ImageThumbnail key={image.uid} path={image.path} />)
                })}
            </Row>
            <Row className="justify-content-center">
                <Col xs="auto">
                    <div ref={loadingRef => (this.loadingRef = loadingRef)} style={loadingCss}>
                        ({this.state.numLoaded}/{this.state.images.length})
                    </div>
                </Col>
            </Row>
        </>
        );
    }
}

export default Gallery;
