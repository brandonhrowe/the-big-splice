import React from 'react'

const Thumbnails = props => {
  const {clips} = props
  return (
    <div>
      {clips.map((clip, index) => (
        <div key={index}>
          <img src={`/static/${clip}_Thumbnail.jpg`} alt={`thumbnail_${index}`} />
        </div>
      ))}
    </div>
  )
}

export default Thumbnails
