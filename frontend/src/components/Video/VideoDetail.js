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
                    const newHistory =  await client.updateHistory (authTokens.key, video.id, document.getElementById("myVideo").currentTime);
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
                    {video.frSubtitleUrl && <track label="French" kind="subtitles" srcLang="fr" src={video.frSubtitleUrl} />}
                    {video.enSubtitleUrl && <track label="English" kind="subtitles" srcLang="eng" src={video.enSubtitleUrl} />}
                    {video.ovSubtitleUrl && <track label="OV" kind="subtitles" srcLang="ov" src={video.ovSubtitleUrl} />}
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
            <SubtitleForm
            />

        </div>
    );
};

export default VideoDetail;
