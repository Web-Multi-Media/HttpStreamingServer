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

        CARROUSSEL_SIZE = 4;
        VIDEO_PER_CLICK = 2;
        VIDEO_PER_PAGE = 12;


    constructor(props) {
        super(props);
        this.onNextClick = this.onNextClick.bind(this);
    }

    state ={
        videos: this.props.videos,
        pageCount: 1,
        clickCount: 0
    };

    onNextClick(){
        const numberOfClicks = this.state.clickCount +1;
        const videoDisplayed = this.CARROUSSEL_SIZE + numberOfClicks * this.VIDEO_PER_CLICK;
        if ((videoDisplayed / this.VIDEO_PER_PAGE < this.state.pageCount) && (videoDisplayed % this.VIDEO_PER_PAGE === 10)){
            console.log("APPEL A L'API");
            const nextPage = this.state.pageCount +1;
                djangoAPI.get(`/get_videos?page=${nextPage}`)
                .then((response) => {
                    let video = this.state.videos;
                    console.log(response.data);
                    //this has to be fixed by adjusting the query
                    video.push(...response.data.results);
                    this.setState({
                        videos: video,
                        pageCount: nextPage,
                        clickCount: numberOfClicks
                    });
                });
        }
        else  {
            this.setState({
                clickCount: numberOfClicks
            });
        }
    };

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

