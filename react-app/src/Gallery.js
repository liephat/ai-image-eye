import React, { Component } from 'react';
import ImageThumbnail from './ImageThumbnail';

class Gallery extends React.Component {
    render() {
        return (
        <>
            <ImageThumbnail path="/images/DSC_2418.jpg" />
            <ImageThumbnail path="/images/DSC_2418.jpg" />
            <ImageThumbnail path="/images/DSC_2418.jpg" />
            <ImageThumbnail path="/images/DSC_2418.jpg" />
        </>
        );
    }
}

export default Gallery;
