import React , { useEffect, useState } from 'react';
import { useAuth } from "../context/auth";
import Button from "@material-ui/core/Button";
//import { client } from '../../api/djangoAPI';
import './User.css'

function UserInfo({displayModal, client}) {
  const { setAuthTokens } = useAuth();
  const { authTokens } = useAuth();

  const [userinfo, setUserInfo] = useState(null);
  useEffect( () => {
      async function getInfos() {
          if (authTokens && authTokens.key !== "") {
              const response = await client.getUserInfo();
              setUserInfo(response);
          }
      }
      getInfos();
  }, [authTokens]);


  function logOut() {
    setAuthTokens();
    displayModal(false);
    client.logout()
  }


  return (
    <div className="headerButton" variant="contained">
      {userinfo &&
      <Button onClick={logOut} variant="contained" color="primary">
           {userinfo.username} {"\n"} (Log out)
      </Button> 
      }
    </div>
  );
}

export default UserInfo;