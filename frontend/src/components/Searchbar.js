import React, { useState } from 'react';
import TextField from '@material-ui/core/TextField';
import makeStyles from '@material-ui/core/styles/makeStyles';
import './Searchbar.css';

export default function Searchbar(props) {
    const useStyles = makeStyles((theme) => ({

        input: {
            backgroundColor: "white",
            color: "white",
            padding: 0
        }
    }));

    const inputProps = {
        color: "white | white ",
    };

    const classes = useStyles();
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
                    <label className="searchElement" htmlFor="video-search">Video Search</label>
                    <TextField className={classes.input}
                               onChange={handleChange}
                               placeholder="Search here"
                               value={term}
                    />
                </div>
            </form>
        </div>
    );
}
