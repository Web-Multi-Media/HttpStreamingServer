import React from "react";
import SearchBar from "../Searchbar";
import './Header.css'

export default function Header({handleFormSubmit, displayModal}) {

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
                    <button className="leftBarElement" onClick={displayModal}>Login
                    </button>
            </div>
        </header>
    );
}
