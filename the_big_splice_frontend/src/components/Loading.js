import React from 'react'
import logo from '../BigSplice_icon.svg'

const Loading = props => {
  return (
    <div>
      <h1 className="title">Loading...</h1>
      <img src={logo} className="logo" alt="logo" />
    </div>
  )
}

export default Loading
