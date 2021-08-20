import React, { useState } from "react";
import { useAuth } from "../context/auth";
import Button from "@material-ui/core/Button";


function UpdateVideo( {client}) {

  async function updatedb() {

    try {
      const response = await client.updatevideodb();
      if (response.status === 200) {
        alert("The update was successfly triggered. Please refresh your window in a while \
(This might take a long time, as we reencode content).");
      } else if(response.status === 226) {
        alert("An update is already running. Please refresh your window in a while");
      }
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <Button variant="contained" color="primary" onClick={updatedb} className="headerButton">
      Update videos
    </Button>
  );

};


export default UpdateVideo;