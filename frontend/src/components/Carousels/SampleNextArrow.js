import React from 'react';
import './SampleNextArrow.css'
import CircularProgress from '@material-ui/core/CircularProgress';

const SampleNextArrow = (props) => {
    const { className, style, onClick } = props;
    const isLoading = props.isloading;

    return (
        <label className="">
            <div className={isLoading ? "next-spinner-wheel" : "next-spinner-hidden"}>
                <CircularProgress/>
            </div>
            <div className="arrow back" onClick={onClick}>› </div>
        </label>
      );

    
};
export default SampleNextArrow;
