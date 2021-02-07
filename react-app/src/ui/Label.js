import React from 'react';

class Label extends React.Component {
    constructor(props) {
        super(props);
        this.calculateStyle = this.calculateStyle.bind(this);
    }
    calculateStyle() {
        // TODO: calculate color unique to this label
        return {
            backgroundColor: 'antiquewhite'
        };
    }

    render() {
        return (
            <>
                <div className='label' style={this.calculateStyle()}>
                    {this.props.label.name}
                </div>
            </>
        );
    }
}

export default Label;