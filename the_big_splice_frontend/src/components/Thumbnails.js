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
  const { clips, onSortEnd, createMainFile, loadClips, clearAllFiles } = props;
  return (
    <div>
      <h3>Drag and drop the below images to edit together your movie</h3>
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
      <br />
      <div className="buttons">
        <button className="button" onClick={createMainFile}>
          CREATE YOUR MOVIE
        </button>
        <button className="button" onClick={loadClips}>
          GET NEW CLIPS
        </button>
        <button className="button" onClick={clearAllFiles}>
          HOME
        </button>
      </div>
    </div>
  );
};

export default Thumbnails;
