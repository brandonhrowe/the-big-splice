import React, { Component } from "react";
import videojs from "video.js";
import "../video-js.min.css";
import strings from "../strings";

export default class Player extends Component {
  componentDidMount() {
    const { main } = this.props;
    this.player = videojs(this.videoNode, {
      autoplay: true,
      controls: true,
      sources: [{ src: `/media/${main}.mp4`, type: "video/mp4" }]
    });
  }

  componentWillUnmount() {
    if (this.player) {
      this.player.dispose();
    }
  }

  render() {
    const { clearMainFiles } = this.props;
    return (
      <div className="video-component-container">
          <div data-video-js className="video-container">
            <video ref={node => (this.videoNode = node)} className="video-js" />
          </div>
        <br />
        <button className="button player-button" onClick={clearMainFiles}>
          {strings.MAKE_A_NEW_MOVIE()}
        </button>
      </div>
    );
  }
}
