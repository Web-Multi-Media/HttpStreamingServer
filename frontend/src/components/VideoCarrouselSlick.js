import React, { Component } from 'react';
import Slider from "react-slick";
import djangoAPI from "../api/djangoAPI";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../style/style.scss';


class VideoCarrouselSlick extends Component {

    SLIDES_OF_CAROUSEL = 5;

    constructor(props) {
        super(props);
        this.state = {
            videos: this.props.videos,
            carrouselCount: 1,
            apiCallCount: 1,
            pagesTotal: this.props.numberOfPages -1,
            index : 0,
            nextQuery: this.props.nextQuery
        };
        this.afterChangeMethod = this.afterChangeMethod.bind(this);
    };

    componentDidMount() {
        this.djangoApi = new djangoAPI();
    }
    
    componentWillReceiveProps(nextProps) {
        if (nextProps.videos !== this.props.videos) {
            this.setState({
                videos: nextProps.videos,
                carrouselCount: 1,
                apiCallCount: 1,
                pagesTotal: nextProps.numberOfPages - 1,
                nextQuery: nextProps.nextQuery
            });
            this.slider.slickGoTo(0, false);
        }
    }

    /**
     * this method is called by react slick after the slider finish transition
     * used to compute if we need to make new API calls
     * @param index
     * @returns {Promise<void>}
     */
    async afterChangeMethod(index) {
        //index is gave by react slick and correspond to the index of the video on the left (start at 1)
        const nextCarrouselCount = index > this.state.index ? this.state.carrouselCount + 1 : this.state.carrouselCount - 1;
        //we add 5 to index to calcultate the number of videos displayed so far
        const pageCount = (index + this.SLIDES_OF_CAROUSEL) / this.props.videosPerPages;
        if(pageCount === this.state.apiCallCount && pageCount <= this.state.pagesTotal){
            // API call to retrieve more videos when navigating through carousel
            const response = await this.djangoApi.getNextVideos(this.state.nextQuery);
            let videos = this.state.videos;
            videos.push(...response.data.results);
            this.setState({
                videos: videos,
                apiCallCount: this.state.apiCallCount +1,
                carrouselCount: nextCarrouselCount,
                nextQuery: response.data.next
            });
        }
        else{
            this.setState( {carrouselCount: nextCarrouselCount});
        }
    }

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
            return <div>
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
