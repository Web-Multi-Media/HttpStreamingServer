import React, { useEffect, useState } from 'react';

export default function AudioTrackSelector({ audioTracks, video, playerref }) {
    const [selectedValue, setSelectedValue] = useState(0); 

    useEffect(() => {
        playerref.setCurrentTrack((playerref.getTracksFor('audio'))[0]);
        setSelectedValue(0);
    }, [video, audioTracks]);

    const handleChange = event => {
        playerref.setCurrentTrack((playerref.getTracksFor('audio'))[event.target.value]);
        setSelectedValue(event.target.value);
    }

    return (
        < div >
            Audio track:
            <select onChange={handleChange} value={selectedValue}>
                {audioTracks.map((option) => (
                    <option key={option.index} value={option.index}>{option.index} </option>
                ))}
            </select>
        </div>
    )

}