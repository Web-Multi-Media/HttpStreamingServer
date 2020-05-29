import React, { useState } from 'react';
import TextField from '@material-ui/core/TextField';
import makeStyles from '@material-ui/core/styles/makeStyles';
import './Searchbar.css';

export default function Searchbar(props) {



    const [term, setTerm] = useState('');

    const handleChange = (event) => {
        setTerm(event.target.value);
        props.handleFormSubmit(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        props.handleFormSubmit(this.state.term);
    };


    return (
        <div className="search-bar ui segment">
            <form onSubmit={handleSubmit} >
                <div className="field">
                    <h2 className="searchElement">Video Search</h2>
                    <div className="group">
                        <input
                            onChange={handleChange}
                            type="text" required
                        />
                            <span className="highlight"></span>
                            <span className="bar"></span>
                            <label>Movie, Serie</label>
                    </div>
                </div>

            </form>
        </div>
    );
}
