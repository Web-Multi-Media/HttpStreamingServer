import React from 'react';
import '../style/video.css';
import {
    ButtonBack, ButtonFirst, ButtonLast, ButtonNext,
    CarouselProvider, DotGroup, Image, ImageWithZoom, Slide, Slider,
} from "pure-react-carousel";
import 'pure-react-carousel/dist/react-carousel.es.css';
import s from '../style/style.scss';

const VideoCarrousel = ({videos, handleVideoSelect}) => {

    const slider = videos.map((video,vIndex) => {
    return <Slide index={vIndex}>
        <div onClick={() => handleVideoSelect(video)} className="img1-wrap">
        <Image src={video.fields.thumbnail} />
        <div className="overlay">
            <div className="text">{video.fields.name}</div>
        </div>
        </div>
    </Slide>
});

    return (    <CarouselProvider
            visibleSlides={4}
            totalSlides={videos.length}
            step={2}
            naturalSlideWidth={400}
            naturalSlideHeight={500}
            hasMasterSpinner
            infinite
        >

            <div   >
                {videos.length > 0 &&
                    <Slider className={s.slider}>
                        {slider}
                    </Slider>
                }
            </div>
            <ButtonFirst>First</ButtonFirst>
            <ButtonBack>Back</ButtonBack>
            <ButtonNext>Next</ButtonNext>
            <ButtonLast>Last</ButtonLast>
        </CarouselProvider>

    )
};
export default VideoCarrousel;

