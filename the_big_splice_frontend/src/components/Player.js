import React, { Component } from "react";
import videojs from "video.js";
import "../video-js.min.css"

export default class Player extends Component {
  componentDidMount() {
    const {main} = this.props
    this.player = videojs(this.videoNode, {
      autoplay: false,
      controls: true,
      sources: [{ src: `/media/${main}.mp4`, type: "video/mp4" }]
    });
  }

  componentWillUnmount(){
    if (this.player){
      this.player.dispose()
    }
  }

  render() {
    const { clearMainFiles } = this.props;
    return (
      <div>
        <div data-video-js>
          <video ref={node => this.videoNode = node} className="video-js"></video>
        </div>
        <button className="button" onClick={clearMainFiles}>
          MAKE A NEW MOVIE
        </button>
      </div>
    );
  }
}
