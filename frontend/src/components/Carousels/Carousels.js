import React from 'react';
import VideoDetail from '../Video/VideoDetail';
import VideoCarrouselSlick from '../VideoCarrouselSlick';
import SeriesCarousel from '../SeriesCarousel';
import './Carousels.css';
import { AuthContext } from '../context/auth';
import VideoDetail3 from "../Video/VideoDetail3";

export default function Carousels({
    video, handleVideoSelect, setHistoryPager, authTokens,
    historyPager, seriesPager, seriesVideos, moviesPager, moviesVideos,
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
            {seriesVideos.length > 0 && (
                <div className="carrouselContainer">
                    <SeriesCarousel
                        pager={seriesPager}
                        videos={seriesVideos}
                        handleVideoSelect={handleVideoSelect}
                    />
                </div>
            )}
            <div className="carrouselContainer">
                <h4>MOVIES</h4>
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
        </div>
    );
}
