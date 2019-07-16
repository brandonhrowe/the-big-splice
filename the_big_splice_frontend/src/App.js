import React, { Component } from "react";
import axios from "axios";
import Loading from "./components/Loading";
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
  }

  async loadClips() {
    try {
      this.setState({
        isLoading: true
      });
      const { data } = await axios.post("/api/clips/", {});
      console.log("data", data)
      this.setState({
        clips: data.files,
        isLoading: false
      });
      console.log(this.state);
    } catch (error) {
      console.log(error);
    }
  }

  render() {
    const { isLoading } = this.state;
    return (
      <div className="App-header">
        {isLoading ? (
          <Loading />
        ) : (
          <button onClick={this.loadClips}>Click for Clips</button>
        )}
      </div>
    );
  }
}
