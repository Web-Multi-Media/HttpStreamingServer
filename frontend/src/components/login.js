
import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import axios from 'axios';
import { Card, Form, Input, Error } from "./AuthForm";
import { useAuth } from "./context/auth";
import Button from "@material-ui/core/Button";

function Login() {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isError, setIsError] = useState(false);
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const email=""
  const { setAuthTokens } = useAuth();

  function postLogin() {
    const http = axios.create({
      baseURL: process.env.REACT_APP_DJANGO_API,
      responseType: 'json',
    });
    http.post("/rest-auth/login/", {
      username,
      password,
      email,
    }).then(result => {
      if (result.status === 200) {
        setAuthTokens(result.data);
        setLoggedIn(true);
      } else {
        setIsError(true);
      }
    }).catch(e => {
      setIsError(true);
    });
  }

  if (isLoggedIn) {
    return <Redirect to="/" />;
  }

  return (
    <Card>
      <Form>
        <Input
          type="username"
          value={username}
          onChange={e => {
            setUserName(e.target.value);
          }}
          placeholder="email"
        />
        <Input
          type="password"
          value={password}
          onChange={e => {
            setPassword(e.target.value);
          }}
          placeholder="password"
        />
        <Button onClick={postLogin} variant="contained" color="primary">
          Sign In
        </Button>
      </Form>
      <Link to="/signup">Don't have an account?</Link>
        { isError &&<Error>The username or password provided were incorrect!</Error> }
    </Card>
  );
}


export default Login;