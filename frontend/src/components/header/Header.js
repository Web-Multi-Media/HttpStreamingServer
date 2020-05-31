import React from 'react';
import SearchBar from '../Searchbar';
import './Header.css';
import User from '../User';
import { AuthContext, useAuth } from '../context/auth';
import Button from "@material-ui/core/Button";

export default function Header({ handleFormSubmit, displayModal }) {
    const { authTokens } = useAuth();
    console.log('salut', authTokens);
    return (
        <header className="headerBar">

            <h1>
                HOMEMADE NETFLIX
            </h1>

            <div className="leftBar">
                <div className="leftBarElement">
                    <SearchBar
                        handleFormSubmit={handleFormSubmit}
                    />
                </div>
                {!authTokens && (
                    <Button variant="contained" color="primary" className="leftBarElement" onClick={displayModal}>
                        Login
                    </Button>
                )}
                {authTokens && <User />}
            </div>
        </header>
    );
}
