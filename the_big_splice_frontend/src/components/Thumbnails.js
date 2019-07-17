import React from "react";
import { SortableContainer, SortableElement } from "react-sortable-hoc";

const ThumbnailItem = SortableElement(({ clip }) => (
  <div>
    <img src={`/static/${clip}_Thumbnail.jpg`} alt={`thumbnail_${clip}`} />
  </div>
));

const ThumbnailContainer = SortableContainer(({ children }) => {
  return <div className="thumbnails">{children}</div>;
});

const Thumbnails = props => {
  const { clips, onSortEnd } = props;
  return (
    <ThumbnailContainer onSortEnd={onSortEnd} axis="x">
      {clips.map((clip, index) => (
        <ThumbnailItem key={index} index={index} clip={clip} />
      ))}
    </ThumbnailContainer>
  );
};

export default Thumbnails;
