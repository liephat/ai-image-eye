import React from 'react';
import ImageThumbnail from './ImageThumbnail';
import Filter from './ui/Filter';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

class Gallery extends React.Component {

    constructor(props) {
        super(props);
        this._loadMore = this._loadMore.bind(this);
        this.onFilterChanged = this.onFilterChanged.bind(this);
        this.state = {
            images: [],
            numLoaded: 0,
        }
    }

    componentDidMount() {
        /* FIXME
           HTTP request will be redirected to the Flask app because of the
           proxy-setting in package.json. This currently only works when
           using the development server of React.
        */
        this._loadImages(fetch('/api/images/all'));
        this._installScrollObserver();
    }

    _loadImages(fetchFrom) {
        fetchFrom.then(res => res.json()).then(data => {
            console.log(data)
            this.setState({
                images: data,
                numLoaded: 6,
            });
        });
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

    _renderThumbnail(image) {
        return (<ImageThumbnail key={image.image_id}
            path={image.path}
            thumbnail_url={image.thumbnail_url}
            name={image.file}
            labels={image.labels} />)
    }

    _thumbnailColumn(columnIndex, columnCount) {
        return (
            <Col className="text-center">
                {this.state.images.slice(0, this.state.numLoaded).filter((image, i) => {
                    return (i % columnCount) === columnIndex;
                }).map((image, i) => {
                    return this._renderThumbnail(image)
                })}
            </Col>
        )
    }

    onFilterChanged(filterString) {
        if (filterString) {
            this._loadImages(fetch('/api/query/images/' + filterString));
        } else {
            this._loadImages(fetch('/api/images/all'));
        }
    }

    render() {
        const loadingCss = {
            height: "100px",
            margin: "30px",
        }
        return (
        <>
            <Row>
                <Col>
                    <Filter onChange={this.onFilterChanged}/>
                </Col>
            </Row>
            <Row>
                {this._thumbnailColumn(0, 3)}
                {this._thumbnailColumn(1, 3)}
                {this._thumbnailColumn(2, 3)}
            </Row>
            <Row className="justify-content-center">
                <Col xs="auto">
                    <div ref={loadingRef => (this.loadingRef = loadingRef)} style={loadingCss}>
                        ({Math.min(this.state.numLoaded, this.state.images.length)}/{this.state.images.length})
                    </div>
                </Col>
            </Row>
        </>
        );
    }
}

export default Gallery;
