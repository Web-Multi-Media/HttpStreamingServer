import React, {useEffect, useState} from 'react';
import { client } from '../../api/djangoAPI';
import Button from "@material-ui/core/Button";
import './VideoDetail.css'
import VTTConverter from 'srt-webvtt';


function VideoDetail  ({ video, handleVideoSelect, authTokens, setHistoryPager }) {

    const [timer, setTimer] = useState(false);
    const [count, setCount] = useState(0);

    async function HandleNextEpisode(handleVideoSelect, nextEpisodeID) {
        const video = await client.getVideoById(nextEpisodeID);
        handleVideoSelect(video);
    }

    const handleChange = event => {
        let customsub = event.target.value;
        var ext = customsub.substr(customsub.lastIndexOf('.') + 1);
        if(ext != "srt"){
            alert("Only .srt files are supported \n");
            return;
        }
        const vttConverter = new VTTConverter(event.target.files[0]);
        let track = document.createElement("track");
        track.id= "my-sub-track";
        track.kind = "captions";
        track.label = "Custom subtitle";
        track.srclang = "en";
        let video = document.getElementById("myVideo");
        video.appendChild(track);
        vttConverter
        .getURL()
        .then(function(url) { // Its a valid url that can be used further
          var track = document.getElementById('my-sub-track'); // Track element (which is child of a video element)
          var video = document.getElementById('myVideo'); // Main video element
          track.src = url; // Set the converted URL to track's source
          video.textTracks[0].mode = 'show'; // Start showing subtitle to your track
        })
        .catch(function(err) {
          console.error(err);
        })
        
    };


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
            <div className="ui segment">
                <form >
                    <label>
                    Add Custom subtitles:
                    <input type="file" onChange={handleChange} />
                    </label>
                </form>
            </div>
        </div>
    );
};

export default VideoDetail;
