import PropTypes from 'prop-types';
import React, { Component, useRef } from 'react';
import classNames from 'classnames';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowRight } from '@fortawesome/free-solid-svg-icons'
import './SkipButton.css'

const propTypes = {
    player: PropTypes.object,
    className: PropTypes.string,
};

function SkipButton(props) {
    const button = useRef();
    const { player, className, HandleNextEpisode, nextEpisode, handleVideoSelect} = props;
    const handleClick = () => {
        HandleNextEpisode(handleVideoSelect,nextEpisode);
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
                <FontAwesomeIcon size={'2x'} icon={faArrowRight} />
            </a>
            </div>
    );
}


export default SkipButton;

SkipButton.propTypes = propTypes;
