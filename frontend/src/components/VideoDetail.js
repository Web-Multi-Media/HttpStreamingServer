import React from 'react';

const VideoDetail = ({video}) => {
    if (!video) {
        return null;
    }
    return (
        <div>
            <div className='ui embed'>
                <video preload="auto" controls width="320" height="240" key={video.pk}>
                    <source src={video.fields.video_url} title='Video player'/>
                    <track label="French" kind="subtitles" srclang="fr"  src={video.fields.fr_subtitle_url}/>
                    <track label="English" kind="subtitles" srclang="eng"  src={video.fields.en_subtitle_url}/>

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
