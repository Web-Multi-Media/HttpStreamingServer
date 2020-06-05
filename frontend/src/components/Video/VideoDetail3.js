import React, { useEffect, useRef, useState } from 'react';
import './VideoDetail.css';
import {
    Player,
    ControlBar,
    ReplayControl,
    ForwardControl,
    CurrentTimeDisplay,
    TimeDivider,
    PlaybackRateMenuButton,
    VolumeMenuButton, ClosedCaptionButton,
} from 'video-react';
import Button from '@material-ui/core/Button';
import { client } from '../../api/djangoAPI';
import SkipButton from './SkipButton';
import AddDelay from './AddDelay';
import RemoveDelay from './RemoveDelay';

function VideoDetail3({
    video, handleVideoSelect, authTokens, setHistoryPager,
}) {
    const playerRef = useRef();
    const [cont, setCont] = useState({});
    const [timer, setTimer] = useState(false);
    const [activeTextTrack, setActiveTextTrack] = useState('hidden');
    const [count, setCount] = useState(0);


    async function HandleNextEpisode(handleVideoSelect, nextEpisodeID) {
        const video = await client.getVideoById(nextEpisodeID);
        handleVideoSelect(video);
    }

    function startVideo() {
        setTimer(true);
    }

    function canPlay(video) {
        if (video.time > 0) {
            playerRef.current.seek(video.time);
        }
    }
    useEffect(() => {
        if (video) {
            playerRef.current.load(video.videoUrl);
            playerRef.current.subscribeToStateChange(updateState);
        }
    }, [video]);

    const updateState = (ref) => {
        console.log(ref.activeTextTrack);
        console.log(playerRef.current.textTracks);
        if (ref.activeTextTrack && ref.activeTextTrack.mode === "showing") {
            setActiveTextTrack('active');
        }else{
            setActiveTextTrack('hidden');
        }
        setCont(ref);
    };


    useEffect(() => {
        if (timer) {
            const theThimer = setInterval(async () => {
                setCount(count + 1);
                if (authTokens) {
                    const newHistory = await client.updateHistory(authTokens.key, video.id, cont.currentTime);
                    setHistoryPager(newHistory);
                }
            }, 20000);
            return () => {
                clearInterval(theThimer);
            };
        }
    }, [timer, count]);

    if (!video) {
        return null;
    }
    return (
        <div data-vjs-player className="test">
            <div data-vjs-player className="test2">
                <Player
                    ref={playerRef}
                    id="myVideo"
                    onLoadedData={() => { canPlay(video); }}
                    onPlay={() => { startVideo(); }}
                >
                    <source src={video.videoUrl} title="Video player" />
                    {video.frSubtitleUrl !== '' && <track label="French" kind="captions" srcLang="fr" src={video.frSubtitleUrl} />}
                    {video.enSubtitleUrl !== '' && <track label="English" kind="captions" srcLang="eng" src={video.enSubtitleUrl} />}
                    {video.ovSubtitleUrl !== '' && <track label="OV" kind="caption" srcLang="ov" src={video.ovSubtitleUrl} />}
                    <ControlBar autoHide={false}>
                        <ReplayControl seconds={10} order={1.1} />
                        <ForwardControl seconds={30} order={1.2} />
                        <CurrentTimeDisplay order={4.1} />
                        <TimeDivider order={4.2} />
                        <ClosedCaptionButton order={7} />
                        <RemoveDelay order={7} className={activeTextTrack} />
                        <AddDelay order={8} className={activeTextTrack} />
                        {video.nextEpisode
                            && (
                                <SkipButton
                                    order={8}
                                    HandleNextEpisode={HandleNextEpisode}
                                    nextEpisode={video.nextEpisode}
                                    handleVideoSelect={handleVideoSelect}
                                />
                            )}
                    </ControlBar>
                </Player>
                <div className="ui segment">
                    <h4 className="ui header">{video.name}</h4>
                </div>
            </div>
        </div>

    );
}

export default VideoDetail3;
