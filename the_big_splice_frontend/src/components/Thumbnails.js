import React from "react";
import { SortableContainer, SortableElement } from "react-sortable-hoc";

const ThumbnailItem = SortableElement(({ clip }) => (
  <div className="thumbnail-wraper">
    <img src={`/media/${clip}_Thumbnail.jpg`} alt={`thumbnail_${clip}`} />
  </div>
));

const ThumbnailContainer = SortableContainer(({ children }) => {
  return <div className="thumbnails">{children}</div>;
});

const Thumbnails = props => {
  const { clips, onSortEnd } = props;
  return (
    <div className="thumbnail-film-strip outer">
      <div className="thumbnail-film-strip middle">
        <div className="thumbnail-film-strip inner">
          <ThumbnailContainer onSortEnd={onSortEnd} axis="x">
            {clips.map((clip, index) => (
              <ThumbnailItem key={index} index={index} clip={clip} />
            ))}
          </ThumbnailContainer>
        </div>
      </div>
    </div>
  );
};

export default Thumbnails;
