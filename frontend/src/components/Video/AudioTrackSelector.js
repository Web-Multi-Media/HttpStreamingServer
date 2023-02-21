import React, {useEffect, useState} from 'react';
import dashjs from 'dashjs'

export default function AudioTrackSelector({ playerref, video, playerIsInitialized }) {
    const [audioTracks, setAudioTrack] = useState([]);
    const [player, setPlayer] = useState();

    useEffect(() => {
        if (playerIsInitialized) {
            let audiotrack = playerref.getTracksFor("audio");
            console.log(audiotrack);
            setAudioTrack(audiotrack);
        }
    }, [video, playerIsInitialized]);

    const handleChange = event => {
        playerref.setCurrentTrack((playerref.getTracksFor('audio'))[event.target.value]);
    }

    return (
        <div>
        Audio track :
        <select onChange={handleChange}>
        {audioTracks.map((option) => (
                <option value={option.index}>{option.index} </option>
            ))}
        </select>
        </div>
    );
}