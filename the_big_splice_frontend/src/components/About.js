import React from "react";

const About = props => {
  const { toggleModal, loadClips } = props;
  return (
    <div className="about-container">
      <p>
        Given a collection of old film clips, it is up to you to piece them together to make your own film-noir concoction.
      </p>
      <div className="buttons about">
        <button className="button" type="button" onClick={toggleModal}>
          READ MORE
        </button>
        <button className="button" type="button" onClick={loadClips}>
          START
        </button>
      </div>
    </div>
  );
};

export default About;
