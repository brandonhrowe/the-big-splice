import React, { Component } from "react";
import axios from "axios";
import Loading from "./components/Loading";
import Thumbnails from "./components/Thumbnails"
import "./App.css";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      clips: [],
      main: "",
      isLoading: false,
      isPlaying: false
    };
    this.loadClips = this.loadClips.bind(this);
    this.clearFiles = this.clearFiles.bind(this);
    this.createMainFile = this.createMainFile.bind(this);
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
        isLoading: false
      });
      console.log(this.state);
    } catch (error) {
      console.log(error);
    }
  }

  async componentWillUnmount() {
    try {
      const { clips, main } = this.state;
      const { data } = await axios.post("/api/remove/", { clips, main });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async clearFiles() {
    try {
      const { clips, main } = this.state;
      const { data } = await axios.post("/api/remove/", { clips, main });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  render() {
    const { isLoading, clips } = this.state;
    return (
      <div className="App-header">
        {isLoading ? (
          <Loading />
        ) : (
          <div>
            <button onClick={this.loadClips}>Click for Clips</button>
            <button onClick={this.clearFiles}>Clear Clips</button>
            {clips.length && (
              <div>
              <button onClick={this.createMainFile}>Create Your Movie</button>
              <Thumbnails clips={clips}/>
              </div>
            )}
          </div>
        )}
      </div>
    );
  }
}
