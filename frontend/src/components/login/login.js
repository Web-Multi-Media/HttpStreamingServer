import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import axios from 'axios';
import { Card, Form, Input, Button, Error } from "./AuthForm";
import { useAuth } from "../context/auth";
import { client } from '../../api/djangoAPI';
import '../Modal.css'

function Login({toggleModalBox, setDisplayModal}) {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isError, setIsError] = useState(false);
  const [errorMessages, setErrorMessage] = useState([]);
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const { setAuthTokens } = useAuth();

  async function postLogin() {
    const param = {
      'username': username,
      'password': password,
      'email': "",

    };
    try {
      const response = await client.postRequest("/rest-auth/login", null, param);
      if (response.status === 200) {
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
      postLogin();
    }
  }

  if (isLoggedIn) {
    return <Redirect to="/" />;
  }

  return (
    <Card>
      <Form>
          <h1 className="modal__header">  Login</h1>
        <div className="crossContainer">
          <svg className="cross"
               viewBox="0 0 24 24"
               onClick={() => setDisplayModal(false)}
          ><path d="M19 6.41l-1.41-1.41-5.59 5.59-5.59-5.59-1.41 1.41 5.59 5.59-5.59 5.59 1.41 1.41 5.59-5.59 5.59 5.59 1.41-1.41-5.59-5.59z"/><path d="M0 0h24v24h-24z" fill="none"/></svg>
        </div>
        <Input
          className="modal__section"
          type="username"
          value={username}
          onChange={e => {setUserName(e.target.value)}}
          placeholder="username"
          onKeyDown={search}
        />
        <Input
          className="modal__section"
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
        { isError &&<Error> 
          Error: 
          {errorMessages.map(message => <div>{message}</div>)}
        
      </Error> }
    </Card>
  );
}


export default Login;
