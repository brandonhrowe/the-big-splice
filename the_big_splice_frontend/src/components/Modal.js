import React from "react";
import strings from "../strings";

const Modal = props => {
  const { toggleModal, displayModal } = props;
  return (
    <div className={`modal ${displayModal && "displayed"}`}>
      <div className="close-container">
        <span className="close" onClick={toggleModal}>
          &times;
        </span>
      </div>
      <p>{strings.MODAL_DESCRIPTION()}</p>
    </div>
  );
};

export default Modal;
