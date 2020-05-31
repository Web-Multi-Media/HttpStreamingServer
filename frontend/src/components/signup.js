import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import axios from 'axios';
import { Card, Form, Input, Button, Error } from "./AuthForm";
import { useAuth } from "./context/auth";

function Signup({toggleModalBox, setDisplayModal}) {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isError, setIsError] = useState(false);
  const [username, setUserName] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const email = ""
  const { setAuthTokens } = useAuth();

  function postSignup() {
    const http = axios.create({
      baseURL: process.env.REACT_APP_DJANGO_API,
      responseType: 'json',
    });
    http.post("/rest-auth/registration/", {
      username,
      password1,
      password2,
    }).then(result => {
      if (result.status === 201) {
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
      postSignup();
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
        <h1 className="modal__header">  Sign up</h1>
        <Input
          type="username"
          value={username}
          onChange={e => {
            setUserName(e.target.value);
          }}
          placeholder="username"
          onKeyDown={search}

      />
        <Input
          type="password"
          value={password1}
          onChange={e => {
            setPassword1(e.target.value);
          }}
          placeholder="password"
          onKeyDown={search}

        />
        <Input
          type="password"
          value={password2}
          onChange={e => {
            setPassword2(e.target.value);
          }}
          placeholder="confirm password"
          onKeyDown={search}


        />
        <Button onClick={postSignup} variant="contained" color="primary">
          Sign Up
        </Button>
      </Form>

      <Link onClick={toggleModalBox}>Already have an account?</Link>
      { isError &&<Error>The username or password provided were incorrect!</Error> }
    </Card>
  );
}

export default Signup;
