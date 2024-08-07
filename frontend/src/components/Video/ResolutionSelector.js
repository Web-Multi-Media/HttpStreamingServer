import React, {useEffect, useState} from 'react';
import dashjs from 'dashjs'

export default function ResolutionSelector({ playerref, video, playerIsInitialized }) {
    const [resolution, setResolution] = useState([]);
    const [player, setPlayer] = useState();

    useEffect(() => {
        if (playerIsInitialized) {
            let resolution = playerref.getBitrateInfoListFor("video");
            console.log(resolution);
            resolution.unshift({ mediaType: "video", bitrate: "auto", width: "auto", height: "auto", qualityIndex: null})
            setResolution(resolution);
        }
    }, [video, playerIsInitialized]);

    const handleChange = event => {
        if(event.target.value === "auto"){
            console.log("Set auto quality ");
            playerref.updateSettings({ 'streaming': { 'abr': { 'autoSwitchBitrate': { 'video': true } } } });

        }else{
            playerref.updateSettings({ 'streaming': { 'abr': { 'autoSwitchBitrate': { 'video': false } } } });
            console.log("Set quality " + event.target.value);
            playerref.setQualityFor("video", event.target.value)
        }

    }

    return (
        <div>
        Quality :
        <select onChange={handleChange}>
            {resolution.map((option) => (
                <option key={option.height} value={option.qualityIndex}>{option.height} </option>
            ))}
        </select>
        </div>
    );
}