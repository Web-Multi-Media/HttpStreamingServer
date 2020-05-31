import React, { useEffect, useState } from 'react';
import { Route, useHistory, useLocation } from 'react-router-dom';
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
import {getMoviesAndSeries, getUrlVideo} from '../utils/utils';
import Header from "./header/Header";
import './App.css'
import Carousels from "./Carousels/Carousels";

function App(props) {
    var existingTokens;
    try{
        existingTokens = JSON.parse(localStorage.getItem("tokens"));
    }
    catch{
        existingTokens = '';
    }
    const [authTokens, setAuthTokens] = useState(existingTokens);
    const [pager, setPager] = useState(null);
    const [displayModal, setDisplayModal] = useState(false);
    const [toggleModal, setToggleModal] = useState(true);
    const [videos, setVideos] = useState([]);
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [moviesPager, setMoviesPager] = useState(null);
    const [historyPager, setHistoryPager] = useState(null);
    const [seriesPager, setSeriesPager] = useState(null);
    const [moviesVideos, setMoviesVideos] = useState([]);
    const [seriesVideos, setSeriesVideos] = useState([]);
    const location = useLocation();
    const history = useHistory();

    useEffect(() => {
        // Create an scoped async function in the hook
        const fetchData = async () => {
            await Promise.all([
                getMoviesAndSeries(setPager, setVideos, setSeriesPager, setSeriesVideos, setMoviesPager, setMoviesVideos),
                getUrlVideo(location, setSelectedVideo)
            ]);
        };
        async function anyNameFunction() {
            // Set the token for the API client
            client.setToken(authTokens);
            if(authTokens && authTokens.key !== ""){
                const history = await client.getHistory(authTokens.key);
                setHistoryPager(history)
            }
        }    // Execute the created function directly
        anyNameFunction(authTokens);
        fetchData();
    }, [authTokens]);

    const handleVideoSelect = (video) => {
        setSelectedVideo(video);
        if (video) {
            history.push(`/streaming/?video=${video.id}`);
            document.title = video.name;
        }
        // change tab title with the name of the selected video
        window.scrollTo(0, 0);
    };


    const displayModalBox = () =>{
        setDisplayModal(true);
    }
    const toggleModalBox = () =>{
        setToggleModal(!toggleModal);
    }


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




    const setTokens = (data) => {
        localStorage.setItem('tokens', JSON.stringify(data));
        setAuthTokens(data);
    };

    return (
        <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
            <Header
                handleFormSubmit={handleSubmit}
                displayModal={displayModalBox}
            />
            <Carousels
                video={selectedVideo}
                handleVideoSelect={handleVideoSelect}
                setHistoryPager={setHistoryPager}
                authTokens={authTokens}
                historyPager={historyPager}
                seriesPager={seriesPager}
                seriesVideos={seriesVideos}
                moviesPager={moviesPager}
                moviesVideos={moviesVideos}
            />
            {(displayModal && toggleModal) &&
            <Login
                toggleModalBox={toggleModalBox}
                setDisplayModal={setDisplayModal}
            />}
            {(displayModal && !toggleModal) &&
            <Signup
                toggleModalBox={toggleModalBox}
                setDisplayModal={setDisplayModal}
            />}
            <PrivateRoute path="/" component={User}  Token={authTokens}/>
        </AuthContext.Provider>
    );
}

export default App;
