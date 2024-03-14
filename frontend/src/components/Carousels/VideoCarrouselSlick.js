import React from 'react';
import Slider from "react-slick";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../../style/style.scss';
import { useState, useEffect } from 'react';



export default function VideoCarrouselSlick({ pager, videos, handleVideoSelect, reset }) {

    const [index, setIndex] = useState(0);
    const SLIDES_OF_CAROUSEL = 5;

    const chooseIndex = (reset) => {
        if (reset === true) {
            return index;
        }
        return 0;
    };

    const setSeriePagerIndex = (index) => {
        if (pager.type === 'Serie') {
            setIndex(index);
        }
    };

    const afterChangeMethod = async (index) => {
         // Assuming this constant value, adjust as needed

        const isLastPage = (index + SLIDES_OF_CAROUSEL) === videos.length;
        setSeriePagerIndex(index);
        
        if (isLastPage && pager.nextPageUrl) {
            // API call to retrieve more videos when navigating through carousel
            try {
                let updatedPager = { ...pager };
                await updatedPager.getNextPage();
                setIndex(index);
            } catch (error) {
                console.log(error);
            }
        }
    };

    useEffect(() => {
        const index = chooseIndex(reset);
        setIndex(index);
    }, [reset]);

    var settings = {
        dots: true,
        infinite: false,
        speed: 500,
        slidesToShow: SLIDES_OF_CAROUSEL,
        slidesToScroll: 1,
        afterChange: afterChangeMethod,
        nextArrow: <SampleNextArrow />,
        prevArrow: <SamplePrevArrow />,
      };

    return (
      <Slider {...settings}>
            {videos.map((video) => (
                        <div className="video-element" key={video.id}>
                        <div className="video-element2"
                            onClick={() => handleVideoSelect(video)}>
                                <img
                                    className={`img-cover`}
                                    src={video.thumbnail}
                                />
                                <div className={`shadow-element`}>
                                    <p
                                        className={`paragraph-element`}
                                    >{video.name}</p>
                                </div>
                            </div>
                        </div>
                    ))}
      </Slider>
    );
  }