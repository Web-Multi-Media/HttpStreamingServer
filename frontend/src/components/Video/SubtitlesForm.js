import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Button,
    useDisclosure,
    Input,
    Box,
    Text
  } from "@chakra-ui/core";
import React, {useEffect, useState, useRef} from 'react';
import { client } from '../../api/djangoAPI';

import VTTConverter from 'srt-webvtt';


const wait = ms => new Promise(
  (resolve, reject) => setTimeout(resolve, ms)
);

function SubtitleForm ({video, token}){

    const [selectedFiles, setSelectedFiles] = useState(undefined);
    const [subtitleName, setSubtitleName] = useState("Custom Subtitle");
    const [subtitleLanguage, setSubtitleLanguage] = useState("eng");
    const hiddenFileInput = useRef(null);

    const handleClick = event => {
      hiddenFileInput.current.click();
    };

    function SendButton({isFileSelected}) {
      if (isFileSelected) {
        return <Button onClick={handleSubmit}>Send</Button>
      }
      return <Button isDisabled={true} onClick={handleSubmit}>Send</Button>
    }

    function ResyncButton({ video, subtitle }) {
      const [substate, setSubState] = useState("pending")
      if (subtitle.webvtt_sync_url.length > 0) {
        return <Button isDisabled={true}>{subtitle.language}</Button>
      } else if (substate === "loading") {
        return <Button isDisabled={true} style={{backgroundColor: "yellow"}} >{subtitle.language} </Button>
      } else if (substate === "finished") {
        return <Button isDisabled={true} style={{backgroundColor: "green"}} >{subtitle.language} </Button>
      } else if (substate === "failure") {
        return <Button isDisabled={true} style={{backgroundColor: "red"}} >{subtitle.language} </Button>
      } else {
        return <Button onClick={handleResync.bind(this, video.id, subtitle.id, setSubState)}>{subtitle.language}</Button>
      }
    }

    const handleSubtitleChange = event => {
        let customsub = event.target.value;
        var ext = customsub.substr(customsub.lastIndexOf('.') + 1);
        if(ext != "srt"){
            alert("Only .srt files are supported \n");
            return;
        }


        setSubtitleName( event.target.files[0].name);
        const vttConverter = new VTTConverter(event.target.files[0]);
        let track = document.createElement("track");
        track.id= "my-sub-track";
        track.kind = "captions";
        track.label = subtitleName;
        let videoElement = document.getElementById("myVideo");
        videoElement.appendChild(track);
        vttConverter
        .getURL()
        .then(function(url) { // Its a valid url that can be used further
          console.log('url', url)
          track.src = url; // Set the converted URL to track's source
          videoElement.textTracks[0].mode = 'show'; // Start showing subtitle to your track
        })
        .catch(function(err) {
          alert(err);
        })

        setSelectedFiles(event.target.files);
      };

  const handleSubtitleLangChange = event => {
    setSubtitleLanguage(event.target.value);
  };


  const handleSubmit = async (event) => {
      event.preventDefault()
      //console.log("sending subtitle Language " + subtitleLanguage)
      const response = await client.uploadSubtitles(video.id, subtitleLanguage, selectedFiles[0]);
      if (response.status != 201)
          alert("Something went wront, are you connected ?");
      onClose();
  };

  const handleResync = async (videoid, subid, setsubstate) => {
    const response = await client.resyncSubtitle(videoid, subid);
    const task_id = response.data.taskid;
    setsubstate("loading");
    var IntervalHandler = setInterval(async function(){     
      
      const response2 = await client.getTaskStatusByID(task_id);
      if (response2.state === "SUCCESS"){
        setsubstate("finished");
        const sub = await client.getSubtitleById(subid);
        console.log(sub.webvttSyncUrl);
        let track = document.createElement("track");
        track.id = "my-sub-track";
        track.kind = "captions";
        track.label = sub.language + "Synced";
        track.src = sub.webvttSyncUrl;
        let videoElement = document.getElementById("myVideo");
        track.addEventListener("load", function () {
          this.mode = "showing";
          video.textTracks[0].mode = "showing"; // thanks Firefox
        });
        videoElement.appendChild(track);
        clearInterval(IntervalHandler);
      }else if (response2.state === "FAILURE"){
        setsubstate("failure");
        clearInterval(IntervalHandler);
      } 
    
    }, 3000);
    
  };


    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
      <>
        <Button onClick={onOpen}>Handle subtitles</Button>

        <Modal isOpen={isOpen} onClose={onClose} onS isCentered>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader color="black"> Subtitles menu</ModalHeader>
            <ModalCloseButton />
            <ModalBody >
              <Box  mb={4} >
              <Text color="black">Upload your subtitles:</Text>
                <Button onClick={handleClick}>
                  Upload SUB{" "}
                </Button>
                <Input
                  type="file"
                  onChange={handleSubtitleChange}
                  accept=".srt"
                  ref={hiddenFileInput}
                  style={{ display: "none" }}
                />
                <select onChange={handleSubtitleLangChange}>
                  <option value="fra">French</option>
                  <option selected value="eng">
                    English
                  </option>
                </select>
              
                <SendButton isFileSelected={selectedFiles}></SendButton>
              <Text mt={4} color="black">Resync existing subtitles:</Text>
              {!video.subtitles
                ? null
                : video.subtitles.map((sub) => (
                    <ResyncButton video={video} subtitle={sub}>
                    </ResyncButton>
                  ))}
              </Box>
            </ModalBody>

            <ModalFooter>
              <Button  onClick={onClose}>
                Close
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    );
}

export default SubtitleForm;

