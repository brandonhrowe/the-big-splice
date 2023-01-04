import React from "react";
import strings from "../strings";

const About = props => {
  const { toggleModal, loadClips } = props;
  return (
    <div className="about-container">
      <p>
        {strings.ABOUT_DESCRIPTION()}
      </p>
      <div className="buttons about">
        <button className="button" type="button" onClick={toggleModal}>
          {strings.READ_MORE()}
        </button>
        <button className="button" type="button" onClick={loadClips}>
          {strings.START()}
        </button>
      </div>
    </div>
  );
};

export default About;
