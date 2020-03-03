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

    componentWillReceiveProps(nextProps) {
        if (nextProps.videos !== this.props.videos) {
            this.setState({
                pager: nextProps.pager,
                videos: nextProps.videos,
                reset: false
            });
        }
    };

    getSeriesSeason = async (serie) => {
        try {
            await serie.getSeason();
            await serie.getEpisodes(serie.seasons[0]);
            this.setState({
                pager: serie,
                videos: serie.videos,
                series: serie.name,
                seasons: serie.seasons,
                seriesId: serie,
                reset: false
            })
        } catch(error) {
            console.log(error);
        }
    };

    handleSeasonSelect = async (e) => {
        const serie = this.state.pager;
        await serie.getEpisodes(e.target.value);
        this.setState({
             pager: serie,
             videos: serie.videos,
             reset: false
         });
    };

    handleSeriesSelect = async (video) => {
        if (this.state.series === '') {
            await this.getSeriesSeason(video);
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
        this.setState({
            pager: this.state.seriesPager,
            videos: this.state.seriesPager.series,
            series: '',
            season: '',
            episode: '',
            reset: true
        })

    };


    render() {
        return (
            <div>
                <div className="seriesDisplay">
                <h3 className="centerVer" onClick={()=>this.resetSeries()}>SERIES</h3>
                {this.state.series.length > 0 &&
                    <React.Fragment>
                    <span className="centerVer"> > {this.state.series} > </span>
                    <SelectBar
                    seasons = {this.state.seasons}
                    handleSeason= {this.handleSeasonSelect}
                    />
                    </React.Fragment>
                }
                {this.state.episode !== '' &&  <span className="centerVer"> > {this.state.episode}</span>}
                </div>
                {this.state.videos.length > 0 &&
                <div>
                    <VideoCarrouselSlick
                        pager={this.state.pager}
                        videos={this.state.videos}
                        handleVideoSelect={this.handleSeriesSelect}
                        reset={this.state.reset}
                    />
                </div>
                }
            </div>
        );
    }
}
export default SeriesCarousel;
