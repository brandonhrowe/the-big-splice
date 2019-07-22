import React, { Component } from "react";
import axios from "axios";
import Loading from "./components/Loading";
import Thumbnails from "./components/Thumbnails";
import Player from "./components/Player";
import About from "./components/About";
import Modal from "./components/Modal";
import "./App.css";
import arrayMove from "array-move";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      clips: [],
      main: "",
      isLoading: false,
      isPlaying: false,
      displayModal: false
    };
    this.loadClips = this.loadClips.bind(this);
    this.clearAllFiles = this.clearAllFiles.bind(this);
    this.createMainFile = this.createMainFile.bind(this);
    this.clearMainFiles = this.clearMainFiles.bind(this);
    this.clearClipFiles = this.clearClipFiles.bind(this);
    this.onSortEnd = this.onSortEnd.bind(this);
    this.toggleModal = this.toggleModal.bind(this);
  }

  async loadClips() {
    try {
      this.setState({
        isLoading: true
      });
      const {clips, main} = this.state
      await axios.post("/api/all/remove/", { clips, main });
      const { data } = await axios.post("/api/clips/", {});
      this.setState({
        clips: data.files,
        isLoading: false
      });
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
    } catch (error) {
      console.log(error);
    }
  }

  componentDidMount() {
    window.addEventListener("beforeunload", event => {
      event.preventDefault();
      event.returnValue = "Reloading this page means you will lose your movie!";
      const { clips, main } = this.state;
      axios.post("/api/all/remove/", { clips, main });
    });
  }

  async clearAllFiles() {
    try {
      const { clips, main } = this.state;
      await axios.post("/api/all/remove/", { clips, main });
      this.setState({
        clips: [],
        main: "",
        isPlaying: false
      });
    } catch (error) {
      console.log(error);
    }
  }

  async clearMainFiles() {
    try {
      const { main } = this.state;
      await axios.post("/api/final/remove/", { main });
      this.setState({
        main: "",
        isPlaying: false
      });
    } catch (error) {
      console.log(error);
    }
  }

  async clearClipFiles() {
    try {
      const { clips } = this.state;
      await axios.post("/api/clips/remove/", { clips });
      this.setState({
        clips: []
      });
    } catch (error) {
      console.log(error);
    }
  }

  onSortEnd({ oldIndex, newIndex }) {
    this.setState(({ clips }) => ({
      clips: arrayMove(clips, oldIndex, newIndex)
    }));
  }

  toggleModal() {
    this.setState(prevState => ({
      displayModal: !prevState.displayModal
    }));
  }

  render() {
    const { clips, main, isLoading, isPlaying, displayModal } = this.state;
    return (
      <div className={`App-header ${isPlaying && "playing"}`}>
        {!isPlaying && !isLoading ? (
          <h1 className="title" onClick={this.clearAllFiles}>THE BIG SPLICE</h1>
        ) : null}
        {isLoading ? (
          <Loading />
        ) : isPlaying && main ? (
          <Player main={main} clearMainFiles={this.clearMainFiles} />
        ) : (
          <div className="about-button-container">
            {/* <button onClick={this.loadClips}>Click for Clips</button>
            <button onClick={this.clearClipFiles}>Clear Clips</button>
            <button onClick={this.clearAllFiles}>Clear All Files</button> */}
            {clips.length ? (
              <div>
                <Thumbnails clips={clips} onSortEnd={this.onSortEnd} createMainFile={this.createMainFile} loadClips={this.loadClips} clearAllFiles={this.clearAllFiles}/>
              </div>
            ) : (
              <About toggleModal={this.toggleModal} loadClips={this.loadClips}/>
            )}
          </div>
        )}
        <Modal displayModal={displayModal} toggleModal={this.toggleModal} />
      </div>
    );
  }
}
