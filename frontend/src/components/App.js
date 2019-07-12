import React from 'react';
import SearchBar from './Searchbar';
import djangoAPI from '../api/djangoAPI';
import VideoList from './VideoList';
import VideoDetail from './VideoDetail';

class App extends React.Component {
    state = {
        videos: [],
        selectedVideo: null
    }

    handleSubmit = async (termFromSearchBar) => {
        const response = await djangoAPI.get('/search_video/', {
            params: {
                q: termFromSearchBar
            }
        })
        this.setState({
            videos: response.data
        })
    };

    componentDidMount(){
        djangoAPI.get("/get_videos/").then((response)=>{
            console.log(response.data);
            this.setState({
                videos: response.data
            })
        })
    }

    handleVideoSelect = (video) => {
        this.setState({selectedVideo: video})
    }

    render() {
        return (
            <div className='ui container' style={{marginTop: '1em'}}>
                <SearchBar handleFormSubmit={this.handleSubmit}/>
                <div className='ui grid'>
                    <div className="ui column">
                        <div className="eleven wide row">
                            <VideoDetail video={this.state.selectedVideo}/>
                        </div>
                        <div className="five wide row">
                            <VideoList handleVideoSelect={this.handleVideoSelect} videos={this.state.videos}/>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default App;