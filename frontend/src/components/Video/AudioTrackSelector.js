import React, { useEffect, useState } from 'react';

export default function AudioTrackSelector({ audioTracks, video, playerref }) {


    useEffect(() => {
        playerref.setCurrentTrack((playerref.getTracksFor('audio'))[0]);
    }, [video]);

    const handleChange = event => {
        playerref.setCurrentTrack((playerref.getTracksFor('audio'))[event.target.value]);
    }

    return (
        < div >
            Audio track:
            <select onChange={handleChange}>
                {audioTracks.map((option) => (
                    <option value={option.index}>{option.index} </option>
                ))}
            </select>
        </div>
    )

}