import React, { Component } from "react";
import logo from "../BigSplice_icon.svg";
import clock from "../Clock_TheStranger_640x480.gif";

export default class Loading extends Component {
  constructor() {
    super();
    this.state = {
      displayGif: false
    };
  }

  componentDidMount() {
    setInterval(() => {
      this.setState((prevState) => ({
        displayGif: !prevState.displayGif
      }));
    }, 15000);
  }

  render() {
    const { displayGif } = this.state;
    return (
      <div className="loading-container">
        <h1 className="title">Loading...</h1>
        <h3>This could take a minute or so. Please don't detour away!</h3>
        {/* <div className={`gif-container ${displayGif && "visible"}`}>
          <div>
          </div>
          <h3>Don't be a stranger, hang around for a while.</h3>
        </div> */}
        <div className="image-container">
          <img
            src={clock}
            className={`${displayGif && "visible"} gif`}
            alt="The Stranger Clock"
          />
          <img
            src={logo}
            className={`${!displayGif && "visible"} logo bottom`}
            alt="logo"
          />
        </div>
      </div>
    );
  }
}
