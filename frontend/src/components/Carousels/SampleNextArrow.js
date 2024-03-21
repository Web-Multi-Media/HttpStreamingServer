import React from 'react';
import './SampleNextArrow.css'
import CircularProgress from '@material-ui/core/CircularProgress';

const SampleNextArrow = (props) => {
    const { className, style, onClick } = props;
    const isLoading = props.isloading;

    if (isLoading) {
        return (
            <label >› <CircularProgress /></label>
        )
    } else {

        return (
            <label className="arrow back" onClick={onClick}>› </label>
        );
    }
};
export default SampleNextArrow;
