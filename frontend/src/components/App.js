import React, { useEffect, useState } from 'react';
import { Route } from 'react-router-dom';
import queryString from 'query-string';
import SearchBar from './Searchbar';
import VideoDetail from './VideoDetail';
import SeriesCarousel from './SeriesCarousel';
import VideoCarrouselSlick from './VideoCarrouselSlick';
import Login from './login';
import Signup from './signup';
import PrivateRoute from './privateRoute';
import User from './User';
import { AuthContext } from './context/auth';
import { client } from '../api/djangoAPI';

function App(props) {
    // const existingTokens = JSON.parse(localStorage.getItem('tokens'));
    const existingTokens = '';
    const [authTokens, setAuthTokens] = useState(existingTokens);
    const [pager, setPager] = useState(null);
    const [videos, setVideos] = useState([]);
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [moviesPager, setMoviesPager] = useState(null);
    const [seriesPager, setSeriesPager] = useState(null);
    const [moviesVideos, setMoviesVideos] = useState([]);
    const [seriesVideos, setSeriesVideos] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            await Promise.all([
                getMoviesAndSeries(),
                getUrlVideo(),
            ]);
        };

        fetchData();
    }, []);

    const  handleVideoSelect = (video) => {
        console.log("handleVideoSelect"+video);
        setSelectedVideo(video);
        if(video){
            // props.history.push("/streaming/?video=" + video.id);
            document.title = video.name;
        }
        // change tab title with the name of the selected video
        window.scrollTo(0, 0);
    };



    const handleSubmit = async (termFromSearchBar) => {
        // API call to retrieve videos from searchbar
        try {
            const [fetchPager, fetchPager2] = await Promise.all([
                client.searchSeries(termFromSearchBar),
                client.searchMovies(termFromSearchBar),
            ]);
            if (fetchPager.series.length > 0) {
                setSeriesPager(fetchPager);
                setSeriesVideos(fetchPager.series);
            }
            if (fetchPager2.videos.length > 0) {
                setMoviesPager(fetchPager2);
                setMoviesVideos(fetchPager2.videos);
            }
        } catch (error) {
            console.log(error);
        }
    };
    /**
     * retrieve movies and series
     * @returns {Promise<void>}
     */
    const getMoviesAndSeries = async () => {
        try {
            const [fetchPager, fetchPager2] = await Promise.all([
                client.searchSeries(),
                client.searchMovies(),
            ]);
            setPager(fetchPager);
            setVideos(fetchPager.videos);
            setSeriesPager(fetchPager);
            setSeriesVideos(fetchPager.series);
            setMoviesPager(fetchPager2);
            setMoviesVideos(fetchPager2.videos);
        } catch (error) {
            console.log(error);
        }
    };

    /**
     * check in the url if a video is specified
     * load it in the player if exist
     * @returns {Promise<void>}
     */
    const getUrlVideo = async () => {
        // const values = queryString.parse(props.location.search);
        const values = {};
        if (values.video) {
            const id = parseInt(values.video);
            // API call to retrieve current video
            // We look here if a query string for the video is provided, if so load the video
            try {
                const video = await client.getVideoById(id);
                setSelectedVideo(video);
            } catch (error) {
                console.log(error);
            }
        }
    };

    const setTokens = (data) => {
        localStorage.setItem('tokens', JSON.stringify(data));
        setAuthTokens(data);
    };


    return (
        <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
            <div className="ui container" style={{ marginTop: '1em' }}>
                <SearchBar handleFormSubmit={handleSubmit} />
                <div className="ui grid">
                    <div className="ui column">
                        <VideoDetail
                            video={selectedVideo}
                            handleVideoSelect={handleVideoSelect}
                        />
                    </div>
                </div>
                {
                    seriesVideos.length > 0
                    && (
                        <div className="carrouselContainer">
                            <SeriesCarousel
                                pager={seriesPager}
                                videos={seriesVideos}
                                handleVideoSelect={handleVideoSelect}
                            />
                        </div>
                    )
                }
                <div className="carrouselContainer">
                    <h4>MOVIES</h4>
                    <div>

                        {
                            moviesVideos.length > 0
                            && (
                                <VideoCarrouselSlick
                                    pager={moviesPager}
                                    videos={moviesVideos}
                                    handleVideoSelect={handleVideoSelect}
                                />
                            )
                        }
                    </div>
                </div>
            </div>
            <Route path="/login" component={Login} />
            <Route path="/signup" component={Signup} />
            <PrivateRoute path="/" component={User} />
        </AuthContext.Provider>
    );
}

export default App;
