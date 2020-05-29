import React from "react";
import SearchBar from "../Searchbar";
import './Header.css'
import SearchIcon from '@material-ui/icons/Search';

export default function Header({handleFormSubmit}) {

    return (
        <header className="headerBar">

                <h1>
                    HOMEMADE NETFLIX
                </h1>

            <div>
                <SearchBar
                    handleFormSubmit={handleFormSubmit}
                />

            </div>
        </header>
    );
}
