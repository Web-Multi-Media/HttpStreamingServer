import React, { Component } from 'react';
import Slider from "react-slick";
import djangoAPI from "../api/djangoAPI";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../style/style.scss';


class VideoCarrouselSlick extends Component {

    CARROUSSEL_SIZE = 5;
    VIDEO_PER_PAGE = 10;

    constructor(props) {
        super(props);
        this.state = {
            videos: this.props.videos,
            //carrousselCount: Number of time next button is clicked
            carrousselCount: 1,
            apiCallCount: 1,
            pagesTotal: this.props.numberOfPages - 1
        };
        this.afterChangeMethod = this.afterChangeMethod.bind(this);
    };

    componentWillReceiveProps(nextProps) {
        if (nextProps.videos !== this.props.videos) {
            this.setState({
                videos: nextProps.videos,
                carrousselCount: 1,
                apiCallCount: 1,
                pagesTotal: nextProps.numberOfPages - 1
            });
            this.slider.slickGoTo(0, false);
        }
    }

    afterChangeMethod() {
        const nextCarrousselCount = this.state.carrousselCount + 1;
        const pageCount = nextCarrousselCount * this.CARROUSSEL_SIZE / this.VIDEO_PER_PAGE;
        if (pageCount === this.state.apiCallCount && pageCount <= this.state.pagesTotal) {
            const nextApiCount = this.state.apiCallCount + 1;
            djangoAPI.get(`/videos?page=${nextApiCount}`)
                .then((response) => {
                    let video = this.state.videos;
                    video.push(...response.data.results);
                    this.setState({
                        videos: video,
                        apiCallCount: nextApiCount,
                        carrousselCount: nextCarrousselCount
                    });
                });
        }
        else {
            this.setState({ carrousselCount: nextCarrousselCount });
        }
    }

    render() {
        const settings = {
            dots: false,
            infinite: false,
            speed: 500,
            slidesToShow: 5,
            slidesToScroll: 5,
            nextArrow: <SampleNextArrow />,
            prevArrow: <SamplePrevArrow />,
            afterChange: current => this.afterChangeMethod(current)
        };

        const slider = this.state.videos.map((video, vIndex) => {
            return <div><img className='img-cover' onClick={() => this.props.handleVideoSelect(video)} src={video.fields.thumbnail} />
                <p className='paragraph'>{video.fields.name}</p></div>


        });

        return (
            <div>
                <Slider ref={c => (this.slider = c)} {...settings}>
                    {slider}
                </Slider>
            </div>
        );
    }
}
export default VideoCarrouselSlick;
