import PropTypes from 'prop-types';
import React, { Component, useRef } from 'react';
import classNames from 'classnames';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faMinus} from '@fortawesome/free-solid-svg-icons';
import './SkipButton.css';


function RemoveDelay(props) {
    const button = useRef();
    const {
        player, className, HandleNextEpisode, nextEpisode, handleVideoSelect,
    } = props;
    const handleClick = () => {
    };
    const { currentSrc } = player;


    return (
        <div className="icone">
            <a
                ref={button}
                className={classNames(className, {
                    'video-react-control': true,
                    'video-react-button': true,
                })}
                onClick={handleClick}
            >
                <FontAwesomeIcon size="2x" icon={faMinus} />
            </a>
        </div>
    );
}


export default RemoveDelay;
