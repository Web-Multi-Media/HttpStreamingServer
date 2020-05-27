import React from "react";
import { Button } from "./AuthForm";
import { useAuth } from "./context/auth";

function UserInfo(props) {
  const { setAuthTokens } = useAuth();

  function logOut() {
    setAuthTokens();
  }

  console.log(props.Token["key"]);

  return (
    <div>
      <div>Admin Page</div>
      <Button onClick={logOut}>Log out</Button>
    </div>
  );
}

export default UserInfo;