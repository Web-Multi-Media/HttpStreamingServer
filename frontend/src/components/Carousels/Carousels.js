import React from 'react';
import VideoDetail from '../Video/VideoDetail';
import VideoCarrouselSlick from './VideoCarrouselSlick';
import SeriesCarousel from './SeriesCarousel';
import './Carousels.css';
import CircularProgress from '@material-ui/core/CircularProgress';


export default function Carousels({
    video, handleVideoSelect, setHistoryPager, authTokens,
    historyPager, seriesPager, seriesVideos, moviesPager, moviesVideos, isInitialVideoDone
}) {
    return (
        <div className="ui container" style={{ marginTop: '1em' }}>
            <div className="ui grid">
                <div className="ui column">
                    <VideoDetail
                        video={video}
                        handleVideoSelect={handleVideoSelect}
                        setHistoryPager={setHistoryPager}
                        authTokens={authTokens}
                    />
                </div>
            </div>
            {(historyPager && historyPager.videos.length > 0 && authTokens) && (
                <div className="carrouselContainer">
                    <h4>RECENTLY WATCHED</h4>
                    <div>
                        <VideoCarrouselSlick
                            pager={historyPager}
                            videos={historyPager.videos}
                            handleVideoSelect={handleVideoSelect}
                        />
                    </div>
                </div>
            )}
            {((seriesVideos.length === 0 && moviesVideos.length === 0)
              && !isInitialVideoDone) && (
                <div className="CircularProgress">
                   <CircularProgress />
                </div>
            )}
            {seriesVideos.length > 0 && (
                <div className="carrouselContainer">
                    <SeriesCarousel
                        pager={seriesPager}
                        videos={seriesVideos}
                        handleVideoSelect={handleVideoSelect}
                    />
                </div>
            )}
            <div className="carrouselContainer ">
            {moviesVideos.length > 0 && <h4>MOVIES</h4>}
                <div>
                    {moviesVideos.length > 0 && (
                        <VideoCarrouselSlick
                            pager={moviesPager}
                            videos={moviesVideos}
                            handleVideoSelect={handleVideoSelect}
                        />
                    )}
                </div>

            </div>
            {((seriesVideos.length === 0 && moviesVideos.length === 0)
              && isInitialVideoDone) && (
                <div className="EmptyVideos">
                    Your video database is empty. Please click on the Update Video button at the top side of the screen to run an update.
                </div>
            )}
        </div>
    );
}
