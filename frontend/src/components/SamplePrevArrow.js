import React from 'react';


const SamplePrevArrow = (props) => {
    const { onClick } = props;
    return (
        <label className="arrow next"  onClick={onClick}>‹</label>
    );
};
export default SamplePrevArrow;
