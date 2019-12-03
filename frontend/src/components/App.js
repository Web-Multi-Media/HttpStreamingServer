import React from 'react';
import SearchBar from './Searchbar';
import djangoAPI from '../api/djangoAPI';
import VideoDetail from './VideoDetail';
import { withRouter } from "react-router-dom";
import queryString from 'query-string'
import VideoCarrouselSlick from "./VideoCarrouselSlick";


class App extends React.Component {
    state = {
        videos: [],
        selectedVideo: null,
        numberOfPages: 0,
        submitTerm: ''
    };

    handleSubmit = async (termFromSearchBar) => {
        const response = await djangoAPI.get('/search_video/', {
            params: {
                q: termFromSearchBar
            }
        });
        this.setState({
            videos: response.data.results,
            submitTerm: termFromSearchBar
        });
    };

    componentDidMount() {
        var videoFromQueryString = null
        const values = queryString.parse(this.props.location.search);
        if (values.video) {
            var pk = parseInt(values.video);
            djangoAPI.get("videos/" + pk + "/").then((response) => {
                videoFromQueryString = response.data[0];
            });
        }

        djangoAPI.get("videos?page=1").then((response) => {
            //We look here if a query string for the video is provided, if so load the video
            this.setState({
                videos: response.data.results,
                selectedVideo: videoFromQueryString,
                numberOfPages: response.data.num_pages
            });
        });
    };

    handleVideoSelect = (video) => {
        this.setState({ selectedVideo: video });
        this.props.history.push("/streaming/?video=" + video.pk);
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
                <div>
                    {
                        this.state.videos.length > 0 &&
                        <div>
                            <VideoCarrouselSlick
                                videos={this.state.videos}
                                handleVideoSelect={this.handleVideoSelect}
                                searchText={this.state.submitTerm}
                                numberOfPages={this.state.numberOfPages}
                            />
                        </div>
                    }
                </div>
            </div>
        )
    }
}

export default withRouter(App);