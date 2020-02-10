import React, { Component } from 'react';
import '../style/style.scss';
import VideoCarrouselSlick from "./VideoCarrouselSlick";
import fakeData from "../fakeData/videos";
import {client} from "../api/djangoAPI";


class SeriesCarousel extends Component {

    constructor(props) {
        super(props);
        this.state = {
            pager:  this.props.pager,
            videos: this.props.videos,
            series: '',
            seriesPager: this.props.pager,
            season: '',
            seasonPager: null,
            episode: '',
        };
    };

    getSeriesSeason = async (tvShow) => {
        try {
            console.log('tvShow');
            console.log(tvShow);

            const pager = await client.getSeason(tvShow);
            console.log(pager);
            console.log('pager');
            this.setState({
                pager: fakeData.videos.seriesSeason,
                videos: fakeData.videos.seriesSeason.videos,
                seasonPager: fakeData.videos.seriesSeason,
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
                pager: fakeData.videos.seriesEpisodes,
                videos: fakeData.videos.seriesEpisodes.videos,
                season: season
            })
        } catch(error) {
            console.log(error);
        }
    };

    handleSeriesSelect = async (video) => {
        if (this.state.series === '') {
            await this.getSeriesSeason(video.id);
        }
        else if(this.state.season === ''){
            await this.getSeriesEpisodes(video.name);
        }
        else{
            this.props.handleVideoSelect(video);
            this.setState({
                episode: video.name
            });
        }
        // change tab title with the name of the selected video
        document.title = video.name;
    };

    resetSeries = () => {
        this.props.handleVideoSelect();
        this.setState({
            pager: this.state.seriesPager,
            videos: this.state.seriesPager.videos,
            series: '',
            season: '',
            episode: ''
        })

    };

    resetEpisodes = () => {
        this.props.handleVideoSelect();
        this.setState({
            pager: this.state.seasonPager,
            videos: this.state.seasonPager.videos,
            season: '',
            episode: ''
        })
    };


    render() {
        return (
            <div>
                <h3 onClick={()=>this.resetSeries()}>SERIES</h3>
                {this.state.series.length > 0 &&

                        <span onClick={()=>this.resetEpisodes()}> > {this.state.series}</span>

                }
                {this.state.season.length  > 0 &&  <span> > {this.state.season}</span>}
                {this.state.episode.length  > 0 &&  <span> > {this.state.episode}</span>}
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
