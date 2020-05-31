import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import axios from 'axios';
import { Card, Form, Input, Error } from "./AuthForm";
import { useAuth } from "./context/auth";
import Button from "@material-ui/core/Button";
import './Modal.css'

function Login({toggleModalBox, setDisplayModal}) {
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

  function search(event) {
    if(event.keyCode == 13) {
      postLogin();
    }
  }

  if (isLoggedIn) {
    return <Redirect to="/" />;
  }

  return (
    <Card>
      <Form>
        <div className="crossContainer">
          <svg className="cross"
               viewBox="0 0 24 24"
               onClick={() => setDisplayModal(false)}
          ><path d="M19 6.41l-1.41-1.41-5.59 5.59-5.59-5.59-1.41 1.41 5.59 5.59-5.59 5.59 1.41 1.41 5.59-5.59 5.59 5.59 1.41-1.41-5.59-5.59z"/><path d="M0 0h24v24h-24z" fill="none"/></svg>
        </div>
        <Input
          type="username"
          value={username}
          onChange={e => {setUserName(e.target.value)}}
          placeholder="username"
          onKeyDown={search}
        />
        <Input
          type="password"
          value={password}
          onChange={e => {setPassword(e.target.value)}}
          placeholder="password"
          onKeyDown={search}
        />
        <Button onClick={postLogin} variant="contained" color="primary">
          Sign In
        </Button>
      </Form>
      <Link onClick={toggleModalBox}>Don't have an account?</Link>
        { isError &&<Error>The username or password provided were incorrect!</Error> }
    </Card>
  );
}


export default Login;
