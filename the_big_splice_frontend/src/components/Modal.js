import React from "react";

const Modal = props => {
  const { toggleModal, displayModal } = props;
  return (
    <div className={`modal ${displayModal && "displayed"}`}>
      <div className="close-container">
        <span className="close" onClick={toggleModal}>
          &times;
        </span>
      </div>
      <p><strong>THE BIG SPLICE</strong> utilizes <a href="https://archive.org/">The Internet Archive's</a> collection of public domain film noirs in order to produce unique shots and scenes for the user.<br/><br/>Once the clips are ready, the user can drag-and-drop those clips in any order they want for their viewing pleasure. Not satisfied with the results? The user can either try another ordering of the clips or load up brand new ones.<br/><br/>This project was loosely inspired by Guy Maddin, Evan Johnson, and Galen Johnson's interactive project <a href="http://seances.nfb.ca/"><strong>SEANCES</strong></a>.</p>
    </div>
  );
};

export default Modal;
