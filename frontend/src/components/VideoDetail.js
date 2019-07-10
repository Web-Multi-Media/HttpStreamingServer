import React from 'react';

const VideoDetail = ({video}) => {
    if (!video) {
        return null;
    }
    return (
        <div>
            <div className='ui embed'>
                <video controls width="320" height="240" key={video.pk}>
                    <source src={video.fields.baseurl} title='Video player'/>
                </video>
            </div>
            <div className='ui segment'>
                <h4 className='ui header'>{video.fields.name}</h4>
                <p>{video.fields.name}</p>
            </div>
        </div>

    )
}

export default VideoDetail;