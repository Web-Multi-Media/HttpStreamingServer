import React, { Component } from 'react';
import '../style/style.scss';
import VideoCarrouselSlick from "./VideoCarrouselSlick";
import fakeData from "../fakeData/videos";
import {client} from "../api/djangoAPI";
import SelectBar from "./SelectBar";


class SeriesCarousel extends Component {

    constructor(props) {
        super(props);
        this.state = {
            pager:  this.props.pager,
            videos: this.props.videos,
            series: '',
            seriesPager: this.props.pager,
            seasons: [],
            episode: '',
            seriesId: 0
        };
    };

    getSeriesSeason = async (tvShow) => {
        try {
            const pager = await client.getSeason(tvShow);
            console.log(pager);
            console.log('pager');
            this.setState({
                pager: pager,
                videos: pager.videos,
                series: pager.title,
                seasons: pager.seasons,
                seriesId: tvShow
            })
        } catch(error) {
            console.log(error);
        }
    };

    handleSeasonSelect = async (e) => {
        const pager = await client.getEpisodes(this.state.seriesId, e.target.value);
        this.setState({
            pager: pager,
            videos: pager.videos
        })
    };

    handleSeriesSelect = async (video) => {
        if (this.state.series === '') {
            await this.getSeriesSeason(video.id);
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



    render() {
        return (
            <div>
                <h3 onClick={()=>this.resetSeries()}>SERIES</h3>
                {this.state.series.length > 0 &&
                    <div>
                    <span> > {this.state.series}</span>
                    <SelectBar
                    seasons = {this.state.seasons}
                    handleSeason= {this.handleSeasonSelect}
                    />
                    </div>
                }
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
