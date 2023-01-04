import React from "react";
import errorGif from "../Error_Detour.gif";
import strings from "../strings";

const Error = () => {
  return (
    <div className="about-container">
      <h1 className="title-font loading">{strings.ERROR_TITLE()}</h1>
      <div className="image-container">
        <img src={errorGif} className="gif visible" alt="Detour Error" />
        <br />
      </div>
      <p>
        {strings.ERROR_SUBTITLE()}
      </p>
    </div>
  );
};

export default Error;
