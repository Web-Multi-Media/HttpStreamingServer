import Modal from "@material-ui/core/Modal";
import Button from "@material-ui/core/Button";

import React, { useEffect, useState, useRef } from "react";
import { client } from "../../api/djangoAPI";
import { makeStyles } from "@material-ui/core/styles";

import VTTConverter from "srt-webvtt";
import { Input, MenuItem, Select } from "@material-ui/core";

const wait = (ms) => new Promise((resolve, reject) => setTimeout(resolve, ms));

const useStyles = makeStyles((theme) => ({
  paper: {
    position: "absolute",
    color: "black",
    width: 500,
    margin: "auto",

    backgroundColor: theme.palette.background.paper,
    border: "2px solid #000",
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  },
  margin: {
    marginLeft: "5px",
    marginRight: "5px",
  },
  minWidth: {
    minWidth: "100px",
  },
  topMargin: {
    margin: "25px 0",
  },
}));

function getModalStyle() {
  const top = 50;
  const left = 50;

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  };
}
function getBackgroundStyle(substate) {
  let color = "#3f51b5";
  if (substate === "loading") {
    color = "yellow";
  } else if (substate === "finished") {
    color = "green";
  } else if (substate === "failure") {
    color = "red";
  }
  return { backgroundColor: color };
}

function SubtitleForm({ video, token }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [subtitleName, setSubtitleName] = useState("Custom Subtitle");
  const [subtitleLanguage, setSubtitleLanguage] = useState("eng");
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

  const handleSubtitleLangChange = (event) => {
    setSubtitleLanguage(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("sending subtitle Language ", selectedFiles);
    const response = await client.uploadSubtitles(
      video.id,
      subtitleLanguage,
      selectedFiles[0]
    );
    if (response.status != 201)
      alert("Something went wront, are you connected ?");
    // onClose();
  };

  const handleResync = async (videoid, subid, setsubstate) => {
    const response = await client.resyncSubtitle(videoid, subid);
    const task_id = response.data.taskid;
    setsubstate("loading");
    var IntervalHandler = setInterval(async function () {
      const response2 = await client.getTaskStatusByID(task_id);
      if (response2.state === "SUCCESS") {
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
      } else if (response2.state === "FAILURE") {
        setsubstate("failure");
        clearInterval(IntervalHandler);
      }
    }, 3000);
  };

  const [modalStyle] = React.useState(getModalStyle);
  const [open, setOpen] = React.useState(false);
  const [substate, setSubState] = useState("pending");

  const classes = useStyles();

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <div>
        <Button
          type="button"
          onClick={handleOpen}
          variant="contained"
          color="primary"
        >
          Open Modal
        </Button>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="simple-modal-title"
          aria-describedby="simple-modal-description"
        >
          <div style={modalStyle} className={classes.paper}>
            <div className={classes.topMargin}>
              <span color="black">Upload your subtitles:</span>
              <Button
                onClick={handleClick}
                className={`${classes.margin} ${classes.minWidth}`}
                variant="contained"
                color="primary"
              >
                Upload SUB{" "}
              </Button>
              <input
                type="file"
                onChange={handleSubtitleChange}
                accept=".srt"
                ref={hiddenFileInput}
                style={{ display: "none" }}
              />

              <Select
                className={`${classes.margin} ${classes.minWidth}`}
                onChange={handleSubtitleLangChange}
              >
                <MenuItem value="fra">French</MenuItem>
                <MenuItem selected value="eng">
                  English
                </MenuItem>
              </Select>

              <Button
                className={`${classes.margin} ${classes.minWidth}`}
                variant="contained"
                color="primary"
                disabled={selectedFiles.length === 0}
                onClick={handleSubmit}
              >
                Send
              </Button>
            </div>
            <div className={classes.topMargin}>
              <span>Resync existing subtitles:</span>
              {!video.subtitles
                ? null
                : video.subtitles.map((sub) => (
                    <Button
                      className={classes.margin}
                      variant="contained"
                      disabled={sub.webvtt_sync_url.length > 0}
                      style={getBackgroundStyle(substate)}
                      onClick={handleResync.bind(
                        this,
                        video.id,
                        sub.id,
                        setSubState
                      )}
                    >
                      {sub.language}
                    </Button>
                  ))}
            </div>
          </div>
        </Modal>
      </div>
    </>
  );
}

export default SubtitleForm;
