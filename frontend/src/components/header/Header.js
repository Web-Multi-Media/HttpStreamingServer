import React from 'react';
import SearchBar from '../Searchbar';
import './Header.css';
import User from '../login/User';
import { AuthContext, useAuth } from '../context/auth';
import Button from "@material-ui/core/Button";

export default function Header({ handleFormSubmit, displayModal }) {
    const { authTokens } = useAuth();
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
                    <div className="headerButton">
                        <Button variant="contained" color="primary" className="leftBarElement" onClick={() => displayModal(true)}>
                            Login
                        </Button>
                    </div>
                )}
                {authTokens &&
                    <div className="headerButton">
                        <User
                            displayModal={displayModal}
                        />
                    </div>
                        }
            </div>
        </header>
    );
}
