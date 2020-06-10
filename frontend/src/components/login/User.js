import React from "react";
import { useAuth } from "../context/auth";
import Button from "@material-ui/core/Button";
import { client } from '../../api/djangoAPI';
import './User.css'

function UserInfo({displayModal}) {
  const { setAuthTokens } = useAuth();

  async function postlogout() {
    const response = await client.postRequest("/rest-auth/logout", null);
  }

  function logOut() {
    setAuthTokens();
    displayModal(false);
    postlogout();
  }


  return (
        <Button onClick={logOut} variant="contained" color="primary">
            Log out
        </Button>
  );
}

export default UserInfo;