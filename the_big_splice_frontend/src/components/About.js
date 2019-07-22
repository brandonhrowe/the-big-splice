import React from "react";

const About = props => {
  const { toggleModal, loadClips } = props;
  return (
    <div className="about-container">
      <p>
        THE BIG SPLICE is a site to concoct your own mini-film. <br />
        Using clips from old film noirs, it is up to YOU to decide on the order
        you want to compile those clips. <br />
        Try any number of combinations until you craft your own hidden gem.
      </p>
      <div className="buttons">
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
