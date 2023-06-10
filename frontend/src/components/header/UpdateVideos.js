import React from "react";
import Button from "@material-ui/core/Button";


function UpdateVideo( {client, updateinfo,  setUpdatedInfo, setCloseUpdateBar }) {

  async function updatedb() {

    try {
      const response = await client.triggerUpdatevideodb();
      if (response.status === 200) {
        const response = await client.getUpdatevideodbState();
        console.log(response);
        setUpdatedInfo(response);
      } else if(response.status === 226) {
        const response = await client.getUpdatevideodbState();
        setUpdatedInfo(response);
      }
      setCloseUpdateBar(true);
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