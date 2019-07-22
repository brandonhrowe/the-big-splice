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
      <br />
      <p>This is stuff that will be in the modal</p>
    </div>
  );
};

export default Modal;
