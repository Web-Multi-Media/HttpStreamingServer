import React from 'react';


const VideoDetail = ({ video }) => {
    if (!video) {
        {console.log('prout 2')}
        return null;
    }
    return (

        <div>
            {console.log('prout')}
            <div className='ui embed'>
                <video preload="auto" controls width="320" height="240" key={video.id}>
                    <source src={video.video_url} title='Video player' />
                    {video.fr_subtitle_url && <track label="French" kind="subtitles" srcLang="fr" src={video.fr_subtitle_url} />}
                    {video.en_subtitle_url && <track label="English" kind="subtitles" srcLang="eng" src={video.en_subtitle_url} />}
                    {video.ov_subtitle_url && <track label="OV" kind="subtitles" srcLang="ov" src={video.ov_subtitle_url} />}
                </video>
            </div>
            <div className='ui segment'>
                <h4 className='ui header'>{video.name}</h4>
            </div>
        </div>
    )
}

export default VideoDetail;
