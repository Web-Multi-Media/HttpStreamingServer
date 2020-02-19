import React from 'react';
import SearchBar from './Searchbar';
import VideoDetail from './VideoDetail';
import { withRouter } from "react-router-dom";
import queryString from 'query-string'
import VideoCarrouselSlick from "./VideoCarrouselSlick";
import { client } from '../api/djangoAPI';
import  fakeData from '../fakeData/videos';
import SeriesCarousel from "./SeriesCarousel";


class App extends React.Component {
    state = {
        pager: null,
        videos: [],
        selectedVideo: null,
        moviesPager:null,
        seriesPager:null,
        moviesVideos :[],
        seriesVideos :[],
    };

    handleSubmit = async (termFromSearchBar) => {
        // API call to retrieve videos from searchbar
        try {

            const [pager, pager2] = await Promise.all([
                client.searchSeries(termFromSearchBar),
                client.searchMovies(termFromSearchBar)
            ]);
            if (pager.series.length > 0){
                this.setState({
                    seriesPager: pager,
                    seriesVideos: pager.series
                });
            }
            if (pager2.videos.length > 0){
                this.setState({
                    moviesPager: pager2,
                    moviesVideos: pager2.videos
                });
            }



        } catch(error) {
            console.log(error);
        }
    };
    /**
     * retrieve movies and series
     * @returns {Promise<void>}
     */
    getMoviesAndSeries = async () => {
        try {
            const [pager, pager2] = await Promise.all([
                client.searchSeries(),
                client.searchMovies()
            ]);
            this.setState({
                pager: pager,
                videos: pager.videos,
                seriesPager:  pager,
                seriesVideos: pager.series,
                moviesPager: pager2,
                moviesVideos: pager2.videos
            });
        } catch(error) {
            console.log(error);
        }
    };

    /**
     * check in the url if a video is specified
     * load it in the player if exist
     * @returns {Promise<void>}
     */
    getUrlVideo = async () => {
        const values = queryString.parse(this.props.location.search);
        if (values.video) {
            let id = parseInt(values.video);
            // API call to retrieve current video
            // We look here if a query string for the video is provided, if so load the video
            try {
                const video = await client.getVideoById(id);
                this.setState({selectedVideo: video})
            } catch(error) {
                console.log(error);
            }
        }
    }

    async componentDidMount() {
        await Promise.all([
            this.getMoviesAndSeries(),
            this.getUrlVideo()
        ]);
    };

    handleVideoSelect = (video) => {
        this.setState({ selectedVideo: video });
        if(video){
            this.props.history.push("/streaming/?video=" + video.id);
            document.title = video.name;
        }
        // change tab title with the name of the selected video
        window.scrollTo(0, 0);
    };

    render() {
        return (
            <div className='ui container' style={{ marginTop: '1em' }}>
                <SearchBar handleFormSubmit={this.handleSubmit} />
                <div className='ui grid'>
                    <div className="ui column">
                        <div className="eleven wide row">
                            <VideoDetail video={this.state.selectedVideo} />
                        </div>
                    </div>
                </div>
                {
                    this.state.seriesVideos.length > 0 &&
                    <div>
                        <SeriesCarousel
                            pager={this.state.seriesPager}
                            videos={this.state.seriesVideos}
                            handleVideoSelect={this.handleVideoSelect}
                        />
                    </div>
                }
                <h4>MOVIES</h4>
                <div>

                    {
                        this.state.moviesVideos.length > 0 &&
                        <div>
                            <VideoCarrouselSlick
                                pager={this.state.moviesPager}
                                videos={this.state.moviesVideos}
                                handleVideoSelect={this.handleVideoSelect}
                            />
                        </div>
                    }
                </div>
            </div>
        )
    }
}

export default withRouter(App);