import React, {Component} from 'react';
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
            carrousselCount: 1,
            apiCallCount: 1,
            pagesTotal: this.props.numberOfPages
        };
        this.afterChangeMethod = this.afterChangeMethod.bind(this);
    };

    afterChangeMethod() {
        const nextCarrousselCount = this.state.carrousselCount +1;
        const pageCount = nextCarrousselCount * this.CARROUSSEL_SIZE / this.VIDEO_PER_PAGE;
        if(pageCount === this.state.apiCallCount && pageCount <= this.state.pagesTotal){
            const nextApiCount = this.state.carrousselCount +1;
            djangoAPI.get(`/get_videos?page=${nextApiCount}`)
                .then((response) => {
                    let video = this.state.videos;
                    //this has to be fixed by adjusting the query
                    video.push(...response.data.results);
                    this.setState({
                        videos: video,
                        apiCallCount: nextApiCount,
                    });
                });
            }
        this.setState( {carrouselCount: nextCarrousselCount});
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
            return <div><img className='img-cover' onClick={() => this.props.handleVideoSelect(video)} src={video.fields.thumbnail}/>
                    <p className='paragraph'>{video.fields.name}</p></div>


        });

        return (
            <div>
                <Slider {...settings}>
                    {slider}
                </Slider>
            </div>
        );
    }
}
export default VideoCarrouselSlick;
