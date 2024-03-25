import React from 'react';
import Slider from "react-slick";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../../style/style.scss';
import { useState, useEffect } from 'react';
import CustomSlider from "./CustomSlider"


export default function VideoCarrouselSlick({ pager, videos, handleVideoSelect, reset, refresh, setRefresh}) {

    const [index, setIndex] = useState(0);
    const [carrouselVideos, setCarrouselVideos] = useState(videos);
    const [isnextpageloading, setIsNextPageLoading] = useState(false);
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
            setIsNextPageLoading(true);
            // API call to retrieve more videos when navigating through carousel
            try {
                let updatedPager = pager ;
                await updatedPager.getNextPage();
                let updatedVideos = [...videos, ...pager.videos];
                setCarrouselVideos(updatedVideos);
                setIndex(index);
            } catch (error) {
                console.log(error);
            }
            setIsNextPageLoading(false);
        }
    };

    useEffect(() => {
        const index = chooseIndex(reset);
        setIndex(index);
    }, [reset]);

    useEffect(() => {
        if (refresh) {
            setCarrouselVideos(videos)
            setRefresh(false)

        }
    }, [refresh]);

    var settings = {
        dots: false,
        infinite: false,
        speed: 500,
        slidesToShow: SLIDES_OF_CAROUSEL,
        slidesToScroll: SLIDES_OF_CAROUSEL,
        //swipeToSlide: true,
        afterChange: afterChangeMethod,
        nextArrow: <SampleNextArrow isloading={isnextpageloading}/>,
        prevArrow: <SamplePrevArrow />,
      };

    return (
      <CustomSlider {...settings}>
            {carrouselVideos.map((video) => (
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
      </CustomSlider>
    );
  }