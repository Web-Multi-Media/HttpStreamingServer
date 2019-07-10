import React from 'react';
import '../style/video.css';

const VideoItem = ({video , handleVideoSelect}) => {
    return (
        <div onClick={ () => handleVideoSelect(video)} className=' video-item item'>
            <video width="10%" key={video.pk}>
                <source src={video.fields.baseurl} title='Video player'/>
            </video>
            <div className='content'>
                <div className='header '>{video.fields.name}</div>
            </div>
        </div>
    )
};
export default VideoItem;