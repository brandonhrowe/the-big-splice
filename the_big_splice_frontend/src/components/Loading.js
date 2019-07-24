import React, { Component } from "react";
import logo from "../BigSplice_icon.svg";
import clock from "../Clock_TheStranger_640x480.gif";
import sleeping from "../Sleeping_Detour_640x480.gif";
import watch from "../Watch_KansasCityConfidential_640x480.gif";

export default class Loading extends Component {
  constructor() {
    super();
    this.state = {
      displayGif: 1
    };
  }

  componentDidMount() {
    setInterval(() => {
      let newGif;
      if (this.state.displayGif === 3) {
        newGif = 1;
      } else {
        newGif = this.state.displayGif + 1;
      }
      this.setState({
        displayGif: newGif
      });
    }, 15000);
  }

  render() {
    const { displayGif } = this.state;
    return (
      <div className="loading-container">
        <h1 className="title-font loading">Loading...</h1>
        <div className="image-container">
          <img
            src={watch}
            className={`${displayGif === 1 && "visible"} gif`}
            alt="Kansas City Confidential Watch"
          />
          <img
            src={clock}
            className={`${displayGif === 2 && "visible"} gif`}
            alt="The Stranger Clock"
          />
          <img
            src={sleeping}
            className={`${displayGif === 3 && "visible"} gif`}
            alt="Detour Sleeping"
          />
          {/* <img
            src={logo}
            className={`${!displayGif && "visible"} logo bottom`}
            alt="logo"
          /> */}
        </div>
        <h3>This could take a minute or so. Please don't detour away!</h3>
      </div>
    );
  }
}
