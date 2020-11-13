import React, { useEffect, useState, useRef } from "react";
import { client } from "../../api/djangoAPI";
import Button from "@material-ui/core/Button";
import "./VideoDetail.css";
import SubtitleForm from "./SubtitlesForm";
import SkipButton from "./SkipButton";
import {
  Player,
  ControlBar,
  ReplayControl,
  ForwardControl,
  CurrentTimeDisplay,
  TimeDivider,
  PlaybackRateMenuButton,
  VolumeMenuButton,
  BigPlayButton,
  ClosedCaptionButton,
} from "video-react";
import UploadSubtitle from "./UploadSubtitle";

function VideoDetail2({
  video,
  handleVideoSelect,
  authTokens,
  setHistoryPager,
}) {
  const [timer, setTimer] = useState(false);
  const [count, setCount] = useState(0);
  const player = useRef();

  useEffect(() => {
    if (video) {
      player.current.load();
    }
  }, [video]);

  async function HandleNextEpisode(handleVideoSelect, nextEpisodeID) {
    const video = await client.getVideoById(nextEpisodeID);
    handleVideoSelect(video);
  }

  function startVideo() {
    setTimer(true);
  }

  useEffect(() => {
    if (timer) {
      const theThimer = setInterval(async () => {
        setCount(count + 1);
        const currentTime = player.current.getState().player.currentTime;

        const newHistory = await client.updateHistory(
          authTokens.key,
          video.id,
          currentTime
        );
        setHistoryPager(newHistory);
      }, 2000);
      return () => {
        clearInterval(theThimer);
      };
    }
  }, [timer, count]);

  if (!video) {
    return null;
  }

  return (
    <div>
      <div className="ui embed">
        <Player
          ref={player}
          width={640}
          height={480}
          fluid={false}
          onPlay={startVideo}
          onPause={() => setTimer(false)}
        >
          <source src={video.videoUrl} title="Video player" />
          {!video.subtitles
            ? null
            : video.subtitles.map((sub, index) => (
                <track
                  label={sub.language}
                  default={index === 0}
                  kind="subtitles"
                  srcLang={sub.language}
                  src={sub.webvtt_subtitle_url}
                />
              ))}
          <BigPlayButton position="center" />
          <ControlBar>
            <ReplayControl seconds={10} order={1.1} />
            <ForwardControl seconds={30} order={1.2} />
            <CurrentTimeDisplay order={4.1} />
            <TimeDivider order={4.2} />
            <PlaybackRateMenuButton rates={[5, 2, 1, 0.5, 0.1]} order={7.1} />
            <ClosedCaptionButton order={7} />
            <VolumeMenuButton />
            {video.nextEpisode && (
              <SkipButton
                HandleNextEpisode={HandleNextEpisode}
                nextEpisode={video.nextEpisode}
                handleVideoSelect={handleVideoSelect}
                order={8}
              />
            )}

            <UploadSubtitle
              video={video}
              token={authTokens}
              order={8}
              player={player}
            />
          </ControlBar>
        </Player>
      </div>
      <div className="ui segment">
        <h4 className="ui header">{video.name}</h4>
      </div>
    </div>
  );
}

export default VideoDetail2;
