import React, { Component } from 'react';
import Slider from "react-slick";
import djangoAPI from "../api/djangoAPI";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../style/style.scss';


class VideoCarrouselSlick extends Component {

    VIDEO_PER_PAGE = 10;

    constructor(props) {
        super(props);
        this.state = {
            videos: this.props.videos,
            //carrousselCount: Number of time next button is clicked
            carrousselCount: 1,
            apiCallCount: 1,
            pagesTotal: this.props.numberOfPages -1,
            index : 0
        };
        this.afterChangeMethod = this.afterChangeMethod.bind(this);
        this.setApICall = this.setApICall.bind(this);
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

    /**
     * Select the call to make to the api depending if the search bar is used or not
     * @param queryText
     * @param nextApiCount
     * @returns {Promise<AxiosResponse<any>>} response from the API call
     */
    async setApICall(queryText, nextApiCount){
        let response;
        if (queryText !== '') {
            response = await djangoAPI.get(`/search_video/?page=${nextApiCount}`, {
                params: {
                    q: queryText
                }
            });
        }
        else {
            response = await djangoAPI.get(`/videos?page=${nextApiCount}`);
        }
        return response;
    }

    /**
     * this method is called by react slick after the slider finish transition
     * used to compute if we need to make new API calls
     * @param index
     * @returns {Promise<void>}
     */
    async afterChangeMethod(index) {
        //index is gave by react slick and correspond to the index of the video on the left (start at 1)
        const nextCarrousselCount = index > this.state.index ? this.state.carrousselCount + 1 : this.state.carrousselCount - 1;
        //we add 5 to index to calcultate the number of videos displayed so far
        const pageCount = (index + 5) / this.VIDEO_PER_PAGE;
        if(pageCount === this.state.apiCallCount && pageCount <= this.state.pagesTotal){
            const response = await this.setApICall(this.props.searchText, this.state.apiCallCount +1);
            let videos = this.state.videos;
            videos.push(...response.data.results);
            this.setState({
                videos: videos,
                apiCallCount: this.state.apiCallCount +1,
                carrousselCount: nextCarrousselCount
            });
        }
        else{
            this.setState( {carrousselCount: nextCarrousselCount});
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
