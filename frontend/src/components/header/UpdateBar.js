import React, { useEffect, useState } from "react";
import './UpdateBar.css';
import '../../style/style.scss'
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { withStyles, makeStyles } from "@material-ui/core/styles";

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

            <div class="UpdateBar">

                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell align="right">Filename</TableCell>
                                <TableCell align="right">processing_state</TableCell>
                                <TableCell align="right">Percentage done</TableCell>
                                <IconButton onClick={() => setCloseUpdateBar(false)} class="CloseButton">
                                    <CloseIcon />
                                </IconButton>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {!updateInfo ? null : Object.entries(updateInfo).map(([key, value]) => {
                                return (
                                    <TableRow key={key} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                        <TableCell align="right">{key}</TableCell>
                                        <TableCell align="right">{updateInfo[key].processing_state}</TableCell>
                                        <TableCell align="right">{updateInfo[key].percentage}</TableCell>
                                    </TableRow>
                                )
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>


            </div>


        </div>
    );

};


export default UpdateBar;