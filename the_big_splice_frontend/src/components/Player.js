import React, { Component } from "react";
import videojs from "video.js";
import "../video-js.min.css"

export default class Player extends Component {
  componentDidMount() {
    const {main} = this.props
    this.player = videojs(this.videoNode, {
      autoplay: false,
      controls: true,
      sources: [{ src: `/static/${main}.mp4`, type: "video/mp4" }]
    }, () => console.log("onPlayerReady", this));
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
        {/* <video controls preload="auto">
          <source src={`/static/${main}.mp4`} type="video/mp4"/>
          <a href={`/static/${main}.mp4`}>Sorry, it looks like your browser can't play this file. Download the
            link here</a>
        </video> */}
        <div data-video-js>
          <video ref={node => this.videoNode = node} className="video-js"></video>
        </div>
        <button onClick={clearMainFiles}>
          Delete This File and Go Back to Clips
        </button>
      </div>
    );
  }
}
