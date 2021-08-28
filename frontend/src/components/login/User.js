import React  from 'react';
import { useAuth } from "../context/auth";
import Button from "@material-ui/core/Button";
//import { client } from '../../api/djangoAPI';
import './User.css'

function UserInfo({displayModal, client, userinfos}) {
  const { setAuthTokens } = useAuth();

  function logOut() {
    setAuthTokens();
    displayModal(false);
    client.logout()
  }


  return (
    <div className="headerButton" variant="contained">
      {userinfos &&
      <Button onClick={logOut} variant="contained" color="primary">
           {userinfos.username} {"\n"} (Log out)
      </Button> 
      }
    </div>
  );
}

export default UserInfo;