import React  from 'react';
import SearchBar from '../Searchbar';
import UpdateVideos from '../Video/UpdateVideos';
import './Header.css';
import User from '../login/User';
import {useAuth } from '../context/auth';
import Button from "@material-ui/core/Button";


export default function Header({ handleFormSubmit, displayModal, client, userinfos , setUserInfos}) {
    const { authTokens } = useAuth();
    return (
        <header className="headerBar">

            <h1>
                <a href="/streaming/">
                HOMEMADE NETFLIX
                </a>
            </h1>

            <div className="leftBar">
                <div className="leftBarElement hideifmobile">
                    {authTokens &&
                    <SearchBar
                        handleFormSubmit={handleFormSubmit}
                    />
                    }
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
                            client={client}
                            userinfos={userinfos}
                        />
                    </div>

                }


                <div className="headerButton hideifmobile">
                {authTokens &&
                    <Button variant="contained" color="primary" className="headerButton">
                        <a href="/transmission/web/">
                            Add Torrent
                        </a>
                    </Button>
                }
                </div>

                <div className="headerButton hideifmobile">
                {authTokens &&
                    <UpdateVideos
                        client={client}
                    />
                }
                </div>

            </div>
        </header>
    );
}
