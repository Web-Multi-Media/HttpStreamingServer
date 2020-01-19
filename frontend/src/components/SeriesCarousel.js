import React, { Component } from 'react';
import '../style/style.scss';
import VideoCarrouselSlick from "./VideoCarrouselSlick";
import fakeData from "../fakeData/videos";


class SeriesCarousel extends Component {

    constructor(props) {
        super(props);
        this.state = {
            pager:  this.props.pager,
            videos: this.props.videos,
            series: '',
            season: 0,
            episode: 0,
        };
    };

    getSeriesSeason = async (tvShow) => {
        try {
            //TODO ADD METHOD TO QUERY SEASONS OF A SERIES
            //const pager = await client.getSeason(tvShow);
            this.setState({
                pager: fakeData.videos.series,
                videos: fakeData.videos.videos,
                series: tvShow
            })
        } catch(error) {
            console.log(error);
        }
    };

    getSeriesEpisodes = async (season) => {
        try {
            //TODO ADD METHOD TO QUERY SEASONS OF A SERIES
            //const pager = await client.getEpisodes(season);
            this.setState({
                pager: fakeData.videos.series,
                videos: fakeData.videos.series.videos,
                season: season
            })
        } catch(error) {
            console.log(error);
        }
    };

    handleSeriesSelect = async (video) => {
        if (this.state.series === '') {
            await this.getSeriesSeason(video.name);
        }
        else if(this.state.season === 0){
            await this.getSeriesEpisodes(video.season);
        }
        else{
            this.props.handleVideoSelect(video);
            this.setState({
                episode: video.episode
            });
        }
        // change tab title with the name of the selected video
        document.title = video.name;
    };

    render() {

        return (
            <div>
                <h4>SERIES</h4>
                {this.state.series.length > 0 &&  <h4> > {this.state.series}</h4>}
                {this.state.season > 0 &&  <h4> > S{this.state.season}</h4>}
                {this.state.episode > 0 &&  <h4> > E{this.state.episode}</h4>}
                {this.state.videos.length > 0 &&
                <div>
                    <VideoCarrouselSlick
                        pager={this.state.pager}
                        videos={this.state.videos}
                        handleVideoSelect={this.handleSeriesSelect}
                    />
                </div>
                }
            </div>
        );
    }
}
export default SeriesCarousel;
