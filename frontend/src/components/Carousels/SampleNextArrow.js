import React from 'react';
import './SampleNextArrow.css'

const SampleNextArrow = (props) => {
    const { onClick } = props;
    return (
        <label className="arrow back" onClick={onClick}>› </label>
    );
};
export default SampleNextArrow;
