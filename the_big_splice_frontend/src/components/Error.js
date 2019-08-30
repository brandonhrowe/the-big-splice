import React from "react";
import errorGif from "../Error_Detour.gif";

const Error = () => {
  return (
    <div className="about-container">
      <h1 className="title-font loading">OH NO!</h1>
      <div className="image-container">
        <img src={errorGif} className="gif visible" alt="Detour Error" />
        <br />
      </div>
      <p>
        Something went a little wrong...
        <br />
        Please try refreshing the page!
      </p>
    </div>
  );
};

export default Error;
