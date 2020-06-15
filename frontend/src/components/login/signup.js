import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import axios from 'axios';
import { Card, Form, Input, Button, Error } from "./AuthForm";
import { useAuth } from "../context/auth";
import { client } from '../../api/djangoAPI';

function Signup({toggleModalBox, setDisplayModal}) {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isError, setIsError] = useState(false);
  const [username, setUserName] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const email = ""
  const { setAuthTokens } = useAuth();
  const [errorMessages, setErrorMessage] = useState([]);

  async function postSignup() {
    const param = {
      'username': username,
      'password1': password1,
      'password2': password2,

    };
    try {
      const response = await client.postRequest("/rest-auth/registration", null, param);
      if (response.status === 201) {
        setAuthTokens(response.data);
        setLoggedIn(true);
      } else {
        setIsError(true);
        setErrorMessage(Object.values(response.data));
      }
    } catch (error) {
      setIsError(true);
      setErrorMessage(Object.values(error.response.data));
    }
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
      { isError &&<Error> 
          Error: 
          {errorMessages.map(message => <div>{message}</div>)}
        
      </Error> }
    </Card>
  );
}

export default Signup;
