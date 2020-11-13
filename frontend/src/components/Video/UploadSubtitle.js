import classNames from "classnames";
import PropTypes from "prop-types";
import React, { useRef, useState } from "react";
import { BiUpload } from "react-icons/bi";
import VTTConverter from "srt-webvtt";
import { client } from "../../api/djangoAPI";
import "./SkipButton.css";
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
} from "@chakra-ui/core";

const propTypes = {
  player: PropTypes.object,
  className: PropTypes.string,
};

function UploadSubtitle(props) {
  const button = useRef();
  const [selectedFiles, setSelectedFiles] = useState(undefined);
  const [subtitleName, setSubtitleName] = useState("Custom Subtitle");
  const hiddenFileInput = useRef(null);

  const handleClick = (event) => {
    hiddenFileInput.current.click();
  };

  const handleSubtitleChange = (event) => {
    let customsub = event.target.value;
    var ext = customsub.substr(customsub.lastIndexOf(".") + 1);
    if (ext != "srt") {
      alert("Only .srt files are supported \n");
      return;
    }

    setSubtitleName(event.target.files[0].name);
    const vttConverter = new VTTConverter(event.target.files[0]);
    let track = document.createElement("track");
    track.id = "my-sub-track";
    track.kind = "captions";
    track.label = subtitleName;
    let videoElement = document.getElementById("myVideo");
    videoElement.appendChild(track);
    vttConverter
      .getURL()
      .then(function (url) {
        // Its a valid url that can be used further
        console.log("url", url);
        track.src = url; // Set the converted URL to track's source
        videoElement.textTracks[0].mode = "show"; // Start showing subtitle to your track
      })
      .catch(function (err) {
        alert(err);
      });

    setSelectedFiles(event.target.files);
  };

  const handleSubtitleNameChange = (event) => {
    setSubtitleName(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (selectedFiles) {
      const response = await client.uploadSubtitles(
        props.token.key,
        props.video.id,
        "eng",
        selectedFiles[0]
      );
    }

    onClose();
  };

  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <div className="icone">
      <a
        ref={button}
        className={classNames(props.className, {
          "video-react-control": true,
          "video-react-button": true,
        })}
        onClick={() => {
          props.player.current.pause();
          onOpen();
        }}
      >
        <BiUpload size="20" color="white" />
      </a>
       {" "}
      <>
        <Modal isOpen={isOpen} onClose={onClose} onS isCentered>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader color="black"> Add Custom subtitles:</ModalHeader>
            <ModalCloseButton />
            <ModalBody mt={4}>
              <Box m={4}>
                <Button mb={4} onClick={handleClick}>
                  Upload SUB{" "}
                </Button>
                <Input
                  type="file"
                  onChange={handleSubtitleChange}
                  accept=".srt"
                  ref={hiddenFileInput}
                  style={{ display: "none" }}
                />
                <Input
                  mb={4}
                  type="text"
                  defaultValue="Custom Subtitle"
                  value={subtitleName}
                  onChange={handleSubtitleNameChange}
                />
              </Box>
            </ModalBody>

            <ModalFooter>
              <Button mb={4} onClick={handleSubmit} mr={3}>
                Send
              </Button>
              <Button variantColor="blue" onClick={onClose}>
                Close
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    </div>
  );
}

export default UploadSubtitle;

UploadSubtitle.propTypes = propTypes;
