import React, {useEffect, useState} from 'react';
import { client } from '../../api/djangoAPI';
import Button from "@material-ui/core/Button";
import './VideoDetail.css'
import SubtitleForm from "./SubtitlesForm"
import dashjs from 'dashjs'
import ResolutionSelector from './ResolutionSelector';
import AudioTrackSelector from './AudioTrackSelector'


function VideoDetail  ({ video, handleVideoSelect, authTokens, setHistoryPager }) {

    const [timer, setTimer] = useState(false);
    const [count, setCount] = useState(0);
    const [player, ] = useState(dashjs.MediaPlayer().create());
    const [playerIsInitialized, setPlayerIsInitialized] = useState(false);
    const [Subtitles, setSubtitles] = useState();
    const [audioTracks, setAudioTrack] = useState([]);
    
    async function HandleNextEpisode(handleVideoSelect, nextEpisodeID) {
        const video = await client.getVideoById(nextEpisodeID);
        handleVideoSelect(video);
    }
    
    
    function startVideo() {
        setTimer(true);
        
    }
    
    function canPlay(video) {
        if (video.time > 0){
            player.seek(video.time);
        }
    }

    useEffect(() => {
        console.log('Video has changed.');
        if (video) {
            if (!playerIsInitialized) {
                player.initialize(document.querySelector("#videoPlayer"), video.videoUrl, true);
                player.on(dashjs.MediaPlayer.events.STREAM_INITIALIZED, () => {
                    setPlayerIsInitialized(true);
                    let audiotrack = player.getTracksFor("audio");
                    //console.log(audiotrack);
                    setAudioTrack(audiotrack);
                });
                setSubtitles(video.subtitles);
            } else {
                player.attachSource(video.videoUrl);
                setSubtitles(video.subtitles);
            }

        }
    }, [video]);
    
    
    useEffect(() => {
        if(timer){
            const theThimer =
            setInterval(async () =>{
                setCount(count + 1);
                const newHistory =  await client.updateHistory (video.id, Math.round( player.time() ));
                setHistoryPager(newHistory);
            }, 20000);
            return () => {
                //console.log('clear');
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
                <div>
                    <video id="videoPlayer" controls
                        onLoadedData={() => { 
                            canPlay(video) }} onPlay={() => { startVideo() 
                        }}
                        onPause={() => setTimer(false)}>
                        <source />
                        {!Subtitles ? null : Subtitles.map((sub, index) =>
                            <>
                                {sub.webvtt_sync_url.length > 0 &&
                                    <track key={sub.webvtt_sync_url} label={`Sync ${sub.language}`} kind="subtitles" default={index === 0 && true} srcLang={sub.language} src={sub.webvtt_sync_url} />
                                }
                                <track key={sub.webvtt_subtitle_url} label={`${sub.language} ${index}`} default={index === 0 && true} kind="subtitles" srcLang={`${sub.language} ${index}`} src={sub.webvtt_subtitle_url} />
                            </>
                        )}
                    </video>
                </div>
            </div>
            <div className="ui segment">
                <h4 className="ui header">{video.name}</h4>
            </div>
            <ResolutionSelector playerref={player} video={video} playerIsInitialized={playerIsInitialized}/>
            {audioTracks.length > 1 &&
                <AudioTrackSelector audioTracks={audioTracks} playerref={player} video={video} playerIsInitialized={playerIsInitialized} />
            }
            <div className="ui segment">
                {video.nextEpisode &&
                    <Button  onClick={() => HandleNextEpisode(handleVideoSelect,video.nextEpisode)} variant="contained" color="primary">
                        Next Episode
                    </Button>
                }
            </div>
            <div className="hideifmobile">
            {authTokens &&
                <SubtitleForm video={video} token={authTokens} handleVideoSelect={handleVideoSelect}/>}
            </div>

        </div>
    );
};

export default VideoDetail;
