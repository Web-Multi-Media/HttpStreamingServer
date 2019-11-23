import React from 'react';
import VideoItem from './VideoCarrousel';
import {ImageWithZoom, Slide} from "pure-react-carousel";


const SampleNextArrow = (props) => {


    const { className, style, onClick } = props;
    return (
        <div
            className={className}
            style={{ ...style, display: "block", background: "green" }}
            onClick= {onClick}
        >
        </div>


    );
};
export default SampleNextArrow;

