import React, {useEffect, useState} from 'react';
import { client } from '../api/djangoAPI';
import Button from "@material-ui/core/Button";




function VideoDetail  ({ video, handleVideoSelect, authTokens, setHistoryPager }) {

    const [timer, setTimer] = useState(false);
    const [count, setCount] = useState(0);

    async function HandleNextEpisode(handleVideoSelect, nextEpisodeID) {
        const video = await client.getVideoById(nextEpisodeID);
        handleVideoSelect(video);
    }

    async function updateHistory(authTokens, id, setHistoryPager) {
        setTimer(true);
        const token = authTokens ? authTokens.key : "";
        if(token !== "") {
            const newHistory = await client.updateHistory (token, id);
            setHistoryPager(newHistory);
        }
    }

    useEffect(() => {
        if(timer){
            const theThimer =
                setInterval(async () =>{
                    setCount(count + 1);
                    await client.updateHistory (authTokens.key, video.id, document.getElementById("myVideo").currentTime);
                }, 100);
            return () => {
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
                <video id="myVideo" preload="auto" controls width="320" height="240" key={video.id} onPlay={()=>{updateHistory(authTokens, video.id, setHistoryPager)} } onPause={() => setTimer(false)}>
                    <source src={video.videoUrl} title='Video player' />
                    {video.frSubtitleUrl && <track label="French" kind="subtitles" srcLang="fr" src={video.frSubtitleUrl} />}
                    {video.enSubtitleUrl && <track label="English" kind="subtitles" srcLang="eng" src={video.enSubtitleUrl} />}
                    {video.ovSubtitleUrl && <track label="OV" kind="subtitles" srcLang="ov" src={video.ovSubtitleUrl} />}
                </video>
            </div>
            <div className="ui segment">
                <h4 className="ui header">{video.name}</h4>
                <h4 className="ui header">{count}</h4>
            </div>
            <div className="ui segment">
                {video.nextEpisode &&
                    <Button  onClick={() => HandleNextEpisode(handleVideoSelect,video.nextEpisode)} variant="contained" color="primary">
                        Next Episode
                    </Button>
                }
            </div>
        </div>
    );
};

export default VideoDetail;
