import React, { useState } from "react";
import { useAuth } from "../context/auth";
import Button from "@material-ui/core/Button";


function UpdateVideo( {client}) {

  async function updatedb() {

    try {
      const response = await client.updatevideodb();
      if (response.status === 200) {
        console.log("cool");
      } else if(response.status === 429) {
        console.log("still cool");
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