import React, {useEffect, useState} from 'react';
import { client } from '../../api/djangoAPI';
import Button from "@material-ui/core/Button";
import './VideoDetail.css'
import SubtitleForm from "./SubtitlesForm"



function VideoDetail  ({ video, handleVideoSelect, authTokens, setHistoryPager }) {

    const [timer, setTimer] = useState(false);
    const [count, setCount] = useState(0);
    
    async function HandleNextEpisode(handleVideoSelect, nextEpisodeID) {
        const video = await client.getVideoById(nextEpisodeID);
        handleVideoSelect(video);
    }
    
    
    function startVideo() {
        setTimer(true);
        
    }
    
    function canPlay(video) {
        console.log('canPlay')
        if (video.time > 0){
            document.getElementById("myVideo").currentTime = video.time;
        }
    }
    
    
    useEffect(() => {
        if(timer){
            const theThimer =
            setInterval(async () =>{
                setCount(count + 1);
                const newHistory =  await client.updateHistory (video.id, document.getElementById("myVideo").currentTime);
                setHistoryPager(newHistory);
            }, 20000);
            return () => {
                console.log('clear');
                clearInterval(theThimer);
            }
        }
    }, [timer, count]);
    
    
    if (!video) {
        return null;
    }


    return (
        
        <div>
            <div className="ui embed">
                <video
                    id="myVideo"
                    preload="auto"
                    controls
                    key={video.id}
                    onLoadedData={()=>{canPlay(video)} } onPlay={()=>{startVideo()} }
                    onPause={() => setTimer(false)}>
                    <source src={video.videoUrl} title='Video player' />
                    {!video.subtitles ? null : video.subtitles.map((sub, index) =>
                        <>
                            {sub.webvtt_sync_url.length > 0 &&
                                <track label={`Sync ${sub.language}`}  kind="subtitles" srcLang={sub.language} src={sub.webvtt_sync_url} />
                            }
                            <track label={sub.language} default={index === 0} kind="subtitles" srcLang={sub.language} src={sub.webvtt_subtitle_url} />
                        </>
                    )}

                    
                </video>
            </div>
            <div className="ui segment">
                <h4 className="ui header">{video.name}</h4>
            </div>
            <div className="ui segment">
                {video.nextEpisode &&
                    <Button  onClick={() => HandleNextEpisode(handleVideoSelect,video.nextEpisode)} variant="contained" color="primary">
                        Next Episode
                    </Button>
                }
            </div>
            {authTokens &&
                <SubtitleForm video={video} token={authTokens} />}

        </div>
    );
};

export default VideoDetail;
