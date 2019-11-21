import React, {Component} from 'react';
import '../style/video.css';
import {
    ButtonBack, ButtonFirst, ButtonLast, ButtonNext,
    CarouselProvider, Image, Slide, Slider,
} from "pure-react-carousel";
import 'pure-react-carousel/dist/react-carousel.es.css';
import '../style/style.scss';
import djangoAPI from "../api/djangoAPI";
import queryString from "query-string";


class VideoCarrousel extends Component{

    constructor(props) {
        super(props);
        this.onNextClick = this.onNextClick.bind(this);
    }

    state ={
        videos: this.props.videos,
        pageCount: 1
    }

    onNextClick(){
        const nextPage = this.state.pageCount +1;
        djangoAPI.get(`/get_videos?page=${nextPage}`)
                .then((response) => {
                    const video = this.state.videos;
                    //this has to be fixed by adjusting the query
                    if (this.state.videos.length < 19){
                    video.push(...response.data);
                    console.log(video);
                    }
                    this.setState(({
                        videos: video,
                        pageCount: nextPage
                    }), () =>  console.log(nextPage)
                    );
        });

    }


    render() {
        const slider = this.state.videos.map((video, vIndex) => {
            return <Slide index={vIndex}>
                <div onClick={() => this.props.handleVideoSelect(video)} className="img1-wrap">
                    <Image src={video.fields.thumbnail}/>
                    <div className="overlay">
                        <div className="text">
                            <p className="paragraph">{video.fields.name}</p>
                        </div>
                    </div>
                </div>
            </Slide>
        });

        return (
            <CarouselProvider
                visibleSlides={4}
                totalSlides={this.props.videos.length}
                step={2}
                naturalSlideWidth={540}
                naturalSlideHeight={320}
                hasMasterSpinner
                infinite
            >
                <div>
                    {this.props.videos.length > 0 &&
                    <Slider>
                        {slider}
                    </Slider>
                    }
                </div>
                <ButtonFirst>First</ButtonFirst>
                <ButtonBack className='_1z3wF right' onClick={this.onPreviousClick}>
                    <svg viewBox="0 0 100 100">
                        <path d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z"/>
                    </svg>
                </ButtonBack>
                <ButtonNext className='_1z3wF left'  onClick={this.onNextClick}>
                    <svg viewBox="0 0 100 100">
                        <path d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z"
                        transform="translate(100, 100) rotate(180)"/>
                    </svg>
                </ButtonNext>
                <ButtonLast>Last</ButtonLast>
            </CarouselProvider>
        )
    }
};
export default VideoCarrousel;

