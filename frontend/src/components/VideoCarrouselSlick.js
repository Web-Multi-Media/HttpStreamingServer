import React, { Component } from 'react';
import Slider from "react-slick";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../style/style.scss';


class VideoCarrouselSlick extends Component {

    //this variable must be the same as PAGE_SIZE in settings.py
    SLIDES_OF_CAROUSEL = 5;

    constructor(props) {
        super(props);
        this.state = {
            pager: this.props.pager,
            videos: this.props.videos
        };
        this.afterChangeMethod = this.afterChangeMethod.bind(this);
    };

    componentWillReceiveProps(nextProps) {
        if (nextProps.videos !== this.props.videos) {
            this.setState({
                pager: nextProps.pager,
                videos: nextProps.videos
            });
            this.slider.slickGoTo(0, false);
        }
    };

    /**
     * this method is called by react slick after the slider finish transition
     * used to compute if we need to make new API calls
     * @param index
     * @returns {Promise<void>}
     */
    async afterChangeMethod(index) {
        const isLastPage = (index + this.SLIDES_OF_CAROUSEL) === this.state.videos.length;
        if (isLastPage && this.state.pager.nextPageUrl){
            // API call to retrieve more videos when navigating through carousel
            try {
                let pager = await this.state.pager.getNextPage();
                let videos = this.state.videos;
                videos.push(...pager.videos);
                this.setState({
                    pager: pager,
                    videos: videos
                });
            } catch(error) {
                // handleError(error);
            }
        }
    };

    render() {
        const settings = {
            dots: false,
            infinite: false,
            speed: 500,
            slidesToShow: this.SLIDES_OF_CAROUSEL,
            slidesToScroll: this.SLIDES_OF_CAROUSEL,
            nextArrow: <SampleNextArrow />,
            prevArrow: <SamplePrevArrow />,
            afterChange: current => this.afterChangeMethod(current)
        };

        const slider = this.state.videos.map((video) => {
            return <div key={video.id}>
                    <img
                        className='img-cover'
                        onClick={() => this.props.handleVideoSelect(video)}
                        src={video.thumbnail}
                    />
                    <p className='paragraph'>{video.name}</p>
                   </div>
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
