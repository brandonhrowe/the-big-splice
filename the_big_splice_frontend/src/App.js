import React, { Component } from "react";
import { Prompt } from "react-router";
import axios from "axios";
import Loading from "./components/Loading";
import Thumbnails from "./components/Thumbnails";
import Player from "./components/Player";
import About from "./components/About";
import "./App.css";
import arrayMove from "array-move";
import createBrowserHistory from "history/createBrowserHistory";
const history = createBrowserHistory();

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
    this.clearAllFiles = this.clearAllFiles.bind(this);
    this.createMainFile = this.createMainFile.bind(this);
    this.clearMainFiles = this.clearMainFiles.bind(this);
    this.clearClipFiles = this.clearClipFiles.bind(this);
    this.onSortEnd = this.onSortEnd.bind(this);
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
      setTimeout(() => {
        this.setState({
          main: data.file,
          isLoading: false,
          isPlaying: true
        });
      }, 2000);
      console.log(this.state);
    } catch (error) {
      console.log(error);
    }
  }

  componentDidMount() {
    window.addEventListener("beforeunload", (event) => {
      event.preventDefault()
      event.returnValue = 'Reloading this page means you will lose your movie!'
      const { clips, main } = this.state;
      axios.post("/api/all/remove/", { clips, main });
    });
  }

  async clearAllFiles() {
    try {
      const { clips, main } = this.state;
      const { data } = await axios.post("/api/all/remove/", { clips, main });
      this.setState({
        clips: [],
        main: "",
        isPlaying: false
      });
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
        main: "",
        isPlaying: false
      });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async clearClipFiles() {
    try {
      const { clips } = this.state;
      const { data } = await axios.post("/api/clips/remove/", { clips });
      this.setState({
        clips: []
      });
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  onSortEnd({ oldIndex, newIndex }) {
    this.setState(({ clips }) => ({
      clips: arrayMove(clips, oldIndex, newIndex)
    }));
  }

  render() {
    const { clips, main, isLoading, isPlaying } = this.state;
    return (
      <div className={`App-header ${isPlaying && "playing"}`}>
        {!isPlaying && !isLoading ? (
          <h1 className="title">THE BIG SPLICE</h1>
        ) : null}
        {isLoading ? (
          <Loading />
        ) : isPlaying && main ? (
          <Player main={main} clearMainFiles={this.clearMainFiles} />
        ) : (
          <div>
            <button onClick={this.loadClips}>Click for Clips</button>
            <button onClick={this.clearClipFiles}>Clear Clips</button>
            <button onClick={this.clearAllFiles}>Clear All Files</button>
            {clips.length ? (
              <div>
                <button onClick={this.createMainFile}>Create Your Movie</button>
                <Thumbnails clips={clips} onSortEnd={this.onSortEnd} />
              </div>
            ) : (
              <About />
            )}
          </div>
        )}
      </div>
    );
  }
}
