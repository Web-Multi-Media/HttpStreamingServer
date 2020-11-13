import PropTypes from "prop-types";
import React, { useRef } from "react";
import classNames from "classnames";
import { BiSkipNext } from "react-icons/bi";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import "./SkipButton.css";

const propTypes = {
  player: PropTypes.object,
  className: PropTypes.string,
};

function SkipButton(props) {
  const button = useRef();
  const {
    className,
    HandleNextEpisode,
    nextEpisode,
    handleVideoSelect,
  } = props;
  const handleClick = () => {
    HandleNextEpisode(handleVideoSelect, nextEpisode);
  };

  return (
    <div className="icone">
      <a
        ref={button}
        className={classNames(className, {
          "video-react-control": true,
          "video-react-button": true,
        })}
        onClick={handleClick}
      >
        <BiSkipNext size="20" color="white" />

        {/* <FontAwesmeIcon size={"2x"} icon={faArrowRight} /> */}
      </a>
       
    </div>
  );
}

export default SkipButton;

SkipButton.propTypes = propTypes;
