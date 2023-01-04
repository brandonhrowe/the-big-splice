import React from "react";
import { SortableContainer, SortableElement } from "react-sortable-hoc";
import strings from "../strings";

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
    <div className="thumbnail-component">
      <h3 className="thumbnail-description">{strings.THUMBNAIL_DESCRIPTION()}</h3>
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
          {strings.CREATE_YOUR_MOVIE()}
        </button>
        <button className="button" onClick={loadClips}>
          {strings.GET_NEW_CLIPS()}
        </button>
        <button className="button" onClick={clearAllFiles}>
          {strings.HOME()}
        </button>
      </div>
    </div>
  );
};

export default Thumbnails;
