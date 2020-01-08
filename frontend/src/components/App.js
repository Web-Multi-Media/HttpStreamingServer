import React from 'react';
import SearchBar from './Searchbar';
import VideoDetail from './VideoDetail';
import { withRouter } from "react-router-dom";
import queryString from 'query-string'
import VideoCarrouselSlick from "./VideoCarrouselSlick";
import { client, handleError } from '../api/djangoAPI';


class App extends React.Component {
    state = {
        videos: [],
        selectedVideo: null,
        numberOfPages: 0,
        videosPerPages: 0,
        submitTerm: '',
        nextQuery: ''
    };

    handleSubmit = async (termFromSearchBar) => {
        // API call to retrieve videos from searchbar
        try {
            const response = await client.searchVideos(termFromSearchBar);
            this.setState({
                videos: response.data.videos,
                numberOfPages: response.data.numberOfPages,
                videosPerPages: response.data.videosPerPages,
                nextQuery: response.data.nextQuery
            });
            console.log('recherche');
        } catch(error) {
            // handleError(error);
        }
    };

    async componentDidMount() {
        const values = queryString.parse(this.props.location.search);
        if (values.video) {
            let id = parseInt(values.video);
            // API call to retrieve current video
            // We look here if a query string for the video is provided, if so load the video
            try {
                const video = await client.getVideoById(id);
                console.log(video)
                this.setState({selectedVideo: video})
            } catch(error) {
                // handleError(error);
            }
        }

        // API call to retrieve all videos
        try {
            const pager = await client.searchVideos();
            console.log(pager.videos);
            
            this.setState({
                pager: pager,
                videos: pager.videos,
                numberOfPages: pager.numberOfPages,
                videosPerPages: pager.videosPerPages,
                // nextQuery: response.data.nextQuery
            });
        } catch(error) {
            // handleError(error);
        }
    };

    handleVideoSelect = (video) => {
        this.setState({ selectedVideo: video });
        this.props.history.push("/streaming/?video=" + video.id);
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
                                pager={this.state.pager}
                                videos={this.state.videos}
                                handleVideoSelect={this.handleVideoSelect}
                                numberOfPages={this.state.numberOfPages}
                                videosPerPages={this.state.videosPerPages}
                                nextQuery={this.state.nextQuery}
                            />
                        </div>
                    }
                </div>
            </div>
        )
    }
}

export default withRouter(App);