import React, { PropsWithChildren, Ref, useState , useEffect} from "react";
import Slider, { Settings as SliderProps } from "react-slick";

//Solution taken from https://github.com/akiran/react-slick/issues/848

/**
 * Threshold from which mouse movement with pressed mouse button
 * is considered a drag instead of a click.
 */
const MoveDragThreshold = 10;


function useDragDetection(){
  const [mouseDown, setMouseDown] = useState(false);
  const [dragging, setDragging] = useState(false);

  useEffect(() => {
    let mouseMove = 0;

    function handleMouseUp() {
      setMouseDown(false);
    }

    function handleMouseMove(e) {
      mouseMove += Math.abs(e.movementX) + Math.abs(e.movementY);
      setDragging(mouseMove > MoveDragThreshold);
    }

    if (mouseDown) {
      document.addEventListener("mouseup", handleMouseUp);
      document.addEventListener("mousemove", handleMouseMove);
    }

    return () => {
      document.removeEventListener("mouseup", handleMouseUp);
      document.removeEventListener("mousemove", handleMouseMove);
    };
  }, [mouseDown]);

  function handleMouseDown(){
    setMouseDown(true);
    setDragging(false);
  }

  return {
    handleMouseDown,
    dragging,
  };
}

export default function CustomSlider(props) {
  const { children, ...sliderProps } = props;

  const {
    handleMouseDown,
    dragging,
  } = useDragDetection();

  function handleChildClick(e) {
    if (dragging) {
      e.preventDefault();
    }
  }

  return (
    <Slider {...sliderProps}>
      {React.Children.map(children, (child) => (
        <div
          onMouseDownCapture={handleMouseDown}
          onClickCapture={handleChildClick}
        >
          {child}
        </div>
      ))}
    </Slider>
  );
}