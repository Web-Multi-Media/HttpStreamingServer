import React from "react";
import { useAuth } from "./context/auth";
import Button from "@material-ui/core/Button";
import './User.css'

function UserInfo(props) {
  const { setAuthTokens } = useAuth();

  function logOut() {
    setAuthTokens();
  }


  return (
        <Button onClick={logOut} variant="contained" color="primary">
            Log out
        </Button>
  );
}

export default UserInfo;