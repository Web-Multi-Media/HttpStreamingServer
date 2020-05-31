import React, { Component } from 'react';
import Slider from "react-slick";
import SampleNextArrow from "./SampleNextArrow";
import SamplePrevArrow from "./SamplePrevArrow";
import '../style/style.scss';


export default  class VideoCarrouselSlick extends Component {

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
        const chooseIndex = (reset) =>{
            if(reset === true){
               return this.state.index;
            }
            return 0;
        };
        if (nextProps.videos !== this.props.videos) {
            const index = chooseIndex(nextProps.reset);
            this.setState({
                pager: nextProps.pager,
                videos: nextProps.videos
            }, () => this.slider.slickGoTo(index, false));
        }
    };


    /**
     * this method is called by react slick after the slider finish transition
     * used to compute if we need to make new API calls
     * @param index
     * @returns {Promise<void>}
     */
    async afterChangeMethod(index) {
        const setSeriePagerIndex = (index) =>{
            if(this.state.pager.type === 'Serie'){
                this.setState({
                    index: index
                });
            }
        };
        const isLastPage = (index + this.SLIDES_OF_CAROUSEL) === this.state.videos.length;
        setSeriePagerIndex(index);
        if (isLastPage && this.state.pager.nextPageUrl){
            // API call to retrieve more videos when navigating through carousel
            try {
                let pager = this.state.pager;
                await pager.getNextPage();
                let videos = this.state.videos;
                videos.push(...pager.videos);
                this.setState({
                    pager: pager,
                    videos: videos
                });
            } catch(error) {
                console.log(error);
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
            return <div className="video-element" key={video.id}>
             <div className="video-element2"
                  onClick={() => this.props.handleVideoSelect(video)}>
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

