import React from 'react';
import '../style/video.css';

const VideoItem = ({video , handleVideoSelect}) => {
    return (
        <div onClick={ () => handleVideoSelect(video)} className=' video-item item'>
            <img src={video.fields.thumbnail} alt="" preload="metadata" key={video.pk}>
            </img>
            <div className='content'>
                <div className='header '>{video.fields.name}</div>
            </div>
        </div>
    )
};
export default VideoItem;