import React, { useState, useEffect } from "react";
import clock from "../Clock_TheStranger_640x480.gif";
import sleeping from "../Sleeping_Detour_640x480.gif";
import watch from "../Watch_KansasCityConfidential_640x480.gif";
import strings from "../strings";

const GIF_CHANGE_INTERVAL = 15000;

const GIFS = [
  {
    src: watch,
    alt: "Kansas City Confidential Watch",
  },
  {
    src: clock,
    alt: "The Stranger Clock",
  },
  {
    src: sleeping,
    alt: "Detour Sleeping",
  },
];

const Loading = () => {
  const [displayGif, setDisplayGif] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      if (displayGif >= GIFS.length - 1) {
        setDisplayGif(0);
      } else {
        setDisplayGif(displayGif + 1);
      }
    }, GIF_CHANGE_INTERVAL);

    return () => {
      clearInterval(interval);
    };
  }, [displayGif]);

  return (
    <div className="loading-container">
      <h1 className="title-font loading">{strings.LOADING_TITLE()}</h1>
      <div className="image-container">
        {/* Separate images are needed to see fade between gifs */}
        {GIFS.map((gif, idx) => (
          <img
            src={gif.src}
            alt={gif.alt}
            className={`${displayGif === idx && "visible"} gif`}
          />
        ))}
      </div>
      <h3>{strings.LOADING_DESCRIPTION()}</h3>
    </div>
  );
};

export default Loading;
