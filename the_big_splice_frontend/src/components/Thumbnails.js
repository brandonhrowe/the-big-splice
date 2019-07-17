import React from 'react'
import {SortableContainer, SortableElement} from 'react-sortable-hoc'

const ThumbnailItem = SortableElement(({clip}) => <img src={`/static/${clip}_Thumbnail.jpg`} alt={`thumbnail_${clip}`} />)

const ThumbnailContainer = SortableContainer(({children}) => {
  return (
    <div className="thumbnails">
      {children}
    </div>
  )
})

// {clips.map((clip, index) => (
//   <ThumbnailItem key={index} index={index} clip={clip}/>
// ))}

const Thumbnails = props => {
  const {clips, onSortEnd} = props
  return (
    <ThumbnailContainer onSortEnd={onSortEnd}>
      {clips.map((clip, index) => (
        <ThumbnailItem key={index} index={index} clip={clip}/>
      ))}
    </ThumbnailContainer>

    // <div className="thumbnails">
    //   {clips.map((clip, index) => (
    //     <div key={index}>
    //       <img src={`/static/${clip}_Thumbnail.jpg`} alt={`thumbnail_${clip}`} />
    //     </div>
    //   ))}
    // </div>
  )
}

export default Thumbnails
