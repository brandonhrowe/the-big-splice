import React, { Component } from "react";
import axios from "axios";
import Loading from "./components/Loading";
import Thumbnails from "./components/Thumbnails";
import Player from "./components/Player";
import About from "./components/About";
import Modal from "./components/Modal";
import Error from "./components/Error";
import "./App.css";
import logo from "./BigSplice_Icon.svg";
import arrayMove from "array-move";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      clips: [],
      main: "",
      isLoading: false,
      isPlaying: false,
      displayModal: false,
      isError: false
    };
    this.loadClips = this.loadClips.bind(this);
    this.clearAllFiles = this.clearAllFiles.bind(this);
    this.createMainFile = this.createMainFile.bind(this);
    this.clearMainFiles = this.clearMainFiles.bind(this);
    this.clearClipFiles = this.clearClipFiles.bind(this);
    this.onSortEnd = this.onSortEnd.bind(this);
    this.toggleModal = this.toggleModal.bind(this);
  }

  componentDidMount() {
    window.addEventListener("beforeunload", event => {
      event.preventDefault();
      event.returnValue = "Reloading this page means you will lose your movie!";
      const { clips, main } = this.state;
      axios.post("/api/files/remove/", { clips, main });
    });
  }

  async loadClips() {
    try {
      this.setState({
        isLoading: true
      });
      const { clips, main } = this.state;
      await axios.post("/api/files/remove/", { clips, main });
      const { data } = await axios.post("/api/clips/", {});
      this.setState({
        clips: data.files,
        isLoading: false
      });
    } catch (error) {
      console.log(error);
      this.setState({
        isError: true,
        isLoading: false
      });
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
      this.setState({
        isError: true,
        isLoading: false
      });
    }
  }

  async clearAllFiles() {
    try {
      const { clips, main } = this.state;
      await axios.post("/api/files/remove/", { clips, main });
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
      await axios.post("/api/files/remove/", { clips: [], main });
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
      await axios.post("/api/files/remove/", { clips, main: "" });
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
    const {
      clips,
      main,
      isLoading,
      isPlaying,
      isError,
      displayModal
    } = this.state;
    return (
      <div className={`App-header ${isPlaying && "playing"}`}>
        {!isError && !isPlaying && !isLoading ? (
          <div className="title-container">
            <img src={logo} className="logo small" alt="logo" />
            <h1 className="title-font title" onClick={this.clearAllFiles}>
              THE BIG SPLICE
            </h1>
            <img src={logo} className="logo small" alt="logo" />
          </div>
        ) : null}
        {isError ? (
          <Error />
        ) : isLoading ? (
          <Loading />
        ) : isPlaying && main ? (
          <Player main={main} clearMainFiles={this.clearMainFiles} />
        ) : (
          <div className="about-button-container">
            {clips.length ? (
              <div>
                <Thumbnails
                  clips={clips}
                  onSortEnd={this.onSortEnd}
                  createMainFile={this.createMainFile}
                  loadClips={this.loadClips}
                  clearAllFiles={this.clearAllFiles}
                />
              </div>
            ) : (
              <About
                toggleModal={this.toggleModal}
                loadClips={this.loadClips}
              />
            )}
          </div>
        )}
        <Modal displayModal={displayModal} toggleModal={this.toggleModal} />
        <div className={`modal-background ${displayModal && "visible"}`}></div>
      </div>
    );
  }
}
