import React, { useState} from 'react';
import SearchBar from '../Searchbar';
import UpdateVideos from './UpdateVideos';
import UpdateBar from './UpdateBar';
import './Header.css';
import './UpdateBar.css'
import User from '../login/User';
import {useAuth } from '../context/auth';
import Button from "@material-ui/core/Button";


export default function Header({ handleFormSubmit, displayModal, client, userinfos, setUserInfos }) {
    const { authTokens } = useAuth();
    const [updateInfo, setUpdatedInfo] = useState(null);
    const [closeUpdateBar, setCloseUpdateBar] = useState(true);
    return (
        <div>
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
                                updateInfo={updateInfo} 
                                setUpdatedInfo={setUpdatedInfo}
                                setCloseUpdateBar={setCloseUpdateBar}
                            />
                        }
                    </div>

                </div>
            </header>
            <header>
                {authTokens && updateInfo && closeUpdateBar &&
                    <UpdateBar client={client} updateInfo={updateInfo}
                        setUpdatedInfo={setUpdatedInfo} setCloseUpdateBar={setCloseUpdateBar} />}
            </header>
        </div>
    );
}
