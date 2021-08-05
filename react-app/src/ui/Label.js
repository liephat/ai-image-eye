import React from 'react';
import { flaskUrl } from '../constants';

class Label extends React.Component {
    constructor(props) {
        super(props);
        this.calculateStyle = this.calculateStyle.bind(this);
        this.updateLabel = this.updateLabel.bind(this);
        this.label_assignment = this.props.label_assignment;
        this.labeled_image = this.props.labeled_image;
    }
    calculateStyle() {
        // TODO: calculate color unique to this label
        let color = 'antiquewhite';
        if (this.label_assignment.label.name === 'unknown_face') {
            color = 'burlywood';
        }
        return {
            backgroundColor: color
        };
    }

    updateLabel() {
        let newName = prompt('New name:');
        if (newName === null || newName === '') {
            return;
        }
        this.label_assignment.label.name = newName;
        console.log(this.label_assignment);

        // Hacked PUT request
        const options = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(this.label_assignment)
        };
        fetch(flaskUrl(this.label_assignment.uri), options)
            .then(response => response.json())
            .then(data => console.log(data));
    }

    render() {
        return (
            <>
                <div
                    className='label' style={this.calculateStyle()}
                    onMouseEnter={() => this.props.startHighlight(this.label_assignment)}
                    onMouseLeave={() => this.props.endHighlight(this.label_assignment)}
                    onClick={this.updateLabel}
                >
                    {this.props.label_assignment.label.name}
                </div>
            </>
        );
    }
}

export default Label;