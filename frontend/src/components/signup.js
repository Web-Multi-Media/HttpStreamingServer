import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import axios from 'axios';
import { Card, Form, Input, Button, Error } from "./AuthForm";
import { useAuth } from "./context/auth";

function Signup() {
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
          placeholder="username"
        />
        <Input
          type="password"
          value={password1}
          onChange={e => {
            setPassword1(e.target.value);
          }}
          placeholder="password"
        />
        <Input
          type="password"
          value={password2}
          onChange={e => {
            setPassword2(e.target.value);
          }}
          placeholder="confirm password"
        />
        <Button onClick={postSignup}>Sign Up</Button>
      </Form>
      <Link to="/login">Already have an account?</Link>
      { isError &&<Error>The username or password provided were incorrect!</Error> }
    </Card>
  );
}

export default Signup;