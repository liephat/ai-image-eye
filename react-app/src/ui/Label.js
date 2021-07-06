import React from 'react';

class Label extends React.Component {
    constructor(props) {
        super(props);
        this.calculateStyle = this.calculateStyle.bind(this);
        this.label_assignment = this.props.label_assignment;
        this.labeled_image = this.props.labeled_image;
    }
    calculateStyle() {
        // TODO: calculate color unique to this label
        let color = 'antiquewhite';
        if (this.label_assignment.label.name === 'person') {
            color = 'burlywood';
        }
        return {
            backgroundColor: color
        };
    }

    render() {
        return (
            <>
                <div
                    className='label' style={this.calculateStyle()}
                    onMouseEnter={() => this.props.startHighlight(this.label_assignment)}
                    onMouseLeave={() => this.props.endHighlight(this.label_assignment)}
                >
                    {this.props.label_assignment.label.name}
                </div>
            </>
        );
    }
}

export default Label;