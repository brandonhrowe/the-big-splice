import React from 'react'

const Player = props => {
  const {main, clearMainFiles} = props
  return (
    <div>
      <video controls preload="metadata">
        <source src={`/static/${main}.mp4`} type="video/mp4"/>
        <a href={`/static/${main}.mp4`}>Sorry, it looks like your browser can't play this file. Download the
          link here</a>
      </video>
      <button onClick={clearMainFiles}>Delete This File and Go Back to Clips</button>
    </div>
  )
}

export default Player
