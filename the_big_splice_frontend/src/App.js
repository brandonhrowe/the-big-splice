import React, { Component } from "react";
import axios from "axios";
import Loading from "./components/Loading";
import Thumbnails from "./components/Thumbnails";
import Player from "./components/Player"
import "./App.css";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      clips: [],
      main: "",
      isLoading: false,
      isPlaying: false,
    };
    this.loadClips = this.loadClips.bind(this);
    this.clearAllFiles = this.clearAllFiles.bind(this);
    this.createMainFile = this.createMainFile.bind(this);
    this.clearMainFiles = this.clearMainFiles.bind(this)
    this.clearClipFiles = this.clearClipFiles.bind(this)
  }

  async loadClips() {
    try {
      this.setState({
        isLoading: true
      });
      const { data } = await axios.post("/api/clips/", {});
      this.setState({
        clips: data.files,
        isLoading: false
      });
      console.log(this.state);
    } catch (error) {
      console.log(error);
    }
  }

  async createMainFile() {
    try {
      this.setState({
        isLoading: true
      });
      const { clips } = this.state;
      const { data } = await axios.post("/api/final/", { files: clips });
      this.setState({
        main: data.file,
        isLoading: false,
        isPlaying: true
      });
      console.log(this.state);
    } catch (error) {
      console.log(error);
    }
  }

  async componentWillUnmount() {
    try {
      const { clips, main } = this.state;
      const { data } = await axios.post("/api/all/remove/", { clips, main });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async clearAllFiles() {
    try {
      const { clips, main } = this.state;
      const { data } = await axios.post("/api/remove/", { clips, main });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async clearMainFiles() {
    try {
      const { main } = this.state;
      const { data } = await axios.post("/api/final/remove/", { main });
      this.setState({
        main: '',
        isPlaying: false
      })
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async clearClipFiles() {
    try {
      const { clips } = this.state;
      const { data } = await axios.post("/api/clips/remove/", { clips });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  render() {
    const { clips, main, isLoading, isPlaying } = this.state;
    return (
      <div className="App-header">
        {isLoading ? (
          <Loading />
        ) : isPlaying && main ? (
          <Player main={main} clearMainFiles={this.clearMainFiles}/>
        ) :
        (
          <div>
            <button onClick={this.loadClips}>Click for Clips</button>
            <button onClick={this.clearClipFiles}>Clear Clips</button>
            <button onClick={this.clearAllFiles}>Clear All Files</button>
            {clips.length ? (
              <div>
                <button onClick={this.createMainFile}>Create Your Movie</button>
                <Thumbnails clips={clips} />
              </div>
            ) : null}
          </div>
        )}
      </div>
    );
  }
}
