import React from 'react';
import Form from 'react-bootstrap/Form';

/**
 * Filter control
 */
class Filter extends React.Component {

    render() {
        return (
            <>
                <Form onKeyPress={(event) => {
                    if (event.key === 'Enter') {
                        // prevent form submission on Enter
                        event.preventDefault();
                    }}}
                    >
                    <Form.Group>
                        <Form.Control
                            onChange={(event) => this.props.onChange(event.target.value)}
                            placeholder="Enter label name (use * as wildcard)"
                        />
                    </Form.Group>
                </Form>
            </>
        );
    }
}

export default Filter;