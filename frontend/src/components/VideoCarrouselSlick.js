import React, {Component} from 'react';
import Slider from "react-slick";
import {Image, Slide} from "pure-react-carousel";
import djangoAPI from "../api/djangoAPI";
import SampleNextArrow from "./SampleNextArrow";



class VideoCarrouselSlick extends Component {

    CARROUSSEL_SIZE = 5;
    VIDEO_PER_CLICK = 4;
    VIDEO_PER_PAGE = 10;

    constructor(props) {
        super(props);
        this.state = {
            videos: this.props.videos,
            pageCount: 1,
            pagesNum: this.props.pagesNum

        };
        this.click = this.click.bind(this);
    };


    click() {
        console.log("APPEL A L'API");
        const nextPage = this.state.pageCount +1;
        djangoAPI.get(`/get_videos?page=${nextPage}`)
            .then((response) => {
                let video = this.state.videos;
                //this has to be fixed by adjusting the query
                video.push(...response.data.results);
                this.setState({
                    videos: video,
                    pageCount: nextPage,
                });
            });
    }



    render() {
        const settings = {
            dots: false,
            infinite: false,
            speed: 500,
            slidesToShow: 5,
            slidesToScroll: 5,
            nextArrow: <SampleNextArrow />,
            afterChange: current => this.click(current)
        };

        const slider = this.state.videos.map((video, vIndex) => {
            return  <div onClick={() => this.props.handleVideoSelect(video)} key={vIndex}>
                        <img src={video.fields.thumbnail}/>
                    </div>

        });
        return (

            <div>
                <h2>Dynamic slides</h2>
                <button className="button" onClick={this.click}>
                    Click to change slide count
                </button>
                <Slider {...settings}>
                    {slider}
                </Slider>
            </div>
        );
    }
}
export default VideoCarrouselSlick;
