import React from 'react';
import VideoItem from './VideoCarrousel';
import {ImageWithZoom, Slide} from "pure-react-carousel";


const VideoList = ({videos , handleVideoSelect}) => {

    if(!videos)
        return null;

    const renderedVideos =  videos.map((video) => {
        return <VideoItem key={video.pk} video={video} handleVideoSelect={handleVideoSelect} />
    });


    return <div className='ui relaxed divided list'>{renderedVideos}</div>;
};
export default VideoList;

