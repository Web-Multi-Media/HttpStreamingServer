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
    Box
  } from "@chakra-ui/core";
import React, {useEffect, useState, useRef} from 'react';
import { client } from '../../api/djangoAPI';

import VTTConverter from 'srt-webvtt';


function SubtitleForm ({video, token}){

    const [selectedFiles, setSelectedFiles] = useState(undefined);
    const [subtitleName, setSubtitleName] = useState("Custom Subtitle");
    const [subtitleLanguage, setSubtitleLanguage] = useState("eng");
    const hiddenFileInput = useRef(null);

    const handleClick = event => {
      hiddenFileInput.current.click();
    };

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



    const handleSubtitleNameChange = event => {
        setSubtitleName(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault()
        //console.log("sending subtitle Language " + subtitleLanguage)
        const response = await client.uploadSubtitles(token.key, video.id, subtitleLanguage, selectedFiles[0]);
        //console.log('r', response)
        if (response.status != 201)
            alert("Something went wront, are you connected ?");
        onClose();
    };

  const handleResync = async (videoid, subid) => {
    console.log(videoid);
    console.log(subid);
    const response = await client.resyncSubtitle(token.key, videoid, subid);
  };


    const { isOpen, onOpen, onClose } = useDisclosure();

    return (

            <>
      <Button onClick={onOpen}>Handle subtitles</Button>

      <Modal isOpen={isOpen} onClose={onClose} onS isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader color="black"> Add Custom subtitles:</ModalHeader>
          <ModalCloseButton />
          <ModalBody mt= {4}>
            <Box m={4}>

              <Button mb={4} onClick={handleClick} >Upload SUB </Button>
              <Input type="file"
                onChange={handleSubtitleChange}
                accept=".srt"
                ref={hiddenFileInput}
                style={{display:'none'}}
                />
              <Input mb={4} type="text" defaultValue="Custom Subtitle" value={subtitleName} onChange={handleSubtitleNameChange}/>
                <select onChange={handleSubtitleLangChange}>
                  <option value="fra">French</option>
                  <option selected value="eng">English</option>
                </select>
                </Box>
                <ModalHeader color="black"> Resync existing subtitle:</ModalHeader>
                    {video.subtitles.map(sub =>
                       <Button mb={4} onClick={handleResync.bind(this, video.id, sub.id)} >{sub.language} </Button>)}
                
          </ModalBody>

          <ModalFooter>
            <Button mb={4} onClick={handleSubmit}  mr={3}>Send</Button>
            <Button variantColor="blue"  onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>

    )
}

export default SubtitleForm;

