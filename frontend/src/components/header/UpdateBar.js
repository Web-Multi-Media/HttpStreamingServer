import React, { useEffect, useState } from "react";
import './UpdateBar.css';
import '../../style/style.scss'
import Button from "@material-ui/core/Button";
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

function UpdateBar({ client ,  updateInfo ,  setUpdatedInfo, setCloseUpdateBar }) {

    const [count, setCount] = useState(0);
    const [timer, setTimer] = useState(false);
    
    
    useEffect(() => {
        if (updateInfo) {
            setTimer(true);
        }
    }, []);

    useEffect(() => {
        if(timer){
            const theThimer =
            setInterval(async () =>{
                setCount(count + 1);
                const response = await client.getUpdatevideodbState();
                setUpdatedInfo(response);
                console.log(theThimer);
                if(response.processing_state === "finished"){
                    clearInterval(theThimer);
                } 
            }, 3000);
            return () => {
                //console.log('clear');
                clearInterval(theThimer);
            }
        }
    }, [timer, count]);

    return (

        <div class="box">

            <div class="UpdateBar">Progress: <h4>state: {updateInfo.processing_state} </h4>
                {updateInfo.processing_file &&
                    <h4>processing file : {updateInfo.processing_file} </h4>}
                {updateInfo.percentage &&
                    <h4>percentage done: {updateInfo.percentage * 100} %</h4>}
                {updateInfo.processing_state === "finished " && <h4> Update is finished, refresh your page</h4>}
            </div>
            <IconButton onClick={() => setCloseUpdateBar(false)} class="CloseButton">
                <CloseIcon />
            </IconButton>
        </div>
    );

};


export default UpdateBar;