import React, {useEffect, useState} from 'react';
import dashjs from 'dashjs'

export default function ResolutionSelector({ playerref, video, playerIsInitialized }) {
    const [resolution, setResolution] = useState([]);
    const [player, setPlayer] = useState();

    useEffect(() => {
        if (playerIsInitialized) {
            let resolution = playerref.getBitrateInfoListFor("video");
            console.log(resolution);
            setResolution(resolution);
        }
    }, [video, playerIsInitialized]);

    const handleChange = event => {    
        playerref.updateSettings({ 'streaming': { 'abr': { 'autoSwitchBitrate': { 'video': false } } } });
        playerref.setQualityFor("video", event.target.value) 
    }

    return (
        <div>
        <select onChange={handleChange}>
            {resolution.map((option) => (
                <option value={option.qualityIndex}>{option.height} p</option>
            ))}
        </select>
        </div>
    );
}