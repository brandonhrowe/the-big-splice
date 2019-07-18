import React, { Component } from "react";
import logo from "../BigSplice_icon.svg";
import clock from "../Clock_TheStranger.gif";

export default class Loading extends Component {
  constructor() {
    super();
    this.state = {
      displayGif: false
    };
  }

  // componentDidMount() {
  //   setTimeout(() => {
  //     this.setState({
  //       displayGif: true
  //     });
  //   }, 10000);
  // }

  render() {
    const { displayGif } = this.state;
    return (
      <div>
        <h1 className="title">Loading...</h1>
        <div className={`gif-container ${displayGif && "visible"}`}>
          <div>
            <img src={clock} alt="The Stranger Clock" />
          </div>
          <h3>Don't be a stranger, hang around for a while.</h3>
        </div>
        <img src={logo} className="logo" alt="logo" />
      </div>
    );
  }
}
