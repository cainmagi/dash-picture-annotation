/**
 * Videos used in the project.
 * Yuchen Jin, mailto:cainmagi@gmail.com
 */

import React, {useEffect} from "react";

import {translate} from "@docusaurus/Translate";

import videojs from "video.js";
import "video.js/dist/video-js.css";

export type VideoJSProps = {
  options: any;
  onReady?: (player: any) => void;
};

export const VideoJS = (props: VideoJSProps) => {
  const videoRef = React.useRef(null);
  const playerRef = React.useRef(null);
  const {options, onReady} = props;

  useEffect(() => {
    // Make sure Video.js player is only initialized once
    if (!playerRef.current) {
      // The Video.js player needs to be _inside_ the component el for React 18 Strict Mode.
      const videoElement = document.createElement("video-js");

      videoElement.classList.add("vjs-big-play-centered");
      videoRef.current.appendChild(videoElement);

      const player = (playerRef.current = videojs(videoElement, options, () => {
        onReady && onReady(player);
      }));

      // You could update an existing player in the `else` block here
      // on prop change, for example:
    } else {
      const player = playerRef.current;

      player.autoplay(options.autoplay);
      player.src(options.sources);
    }
  }, [options, videoRef]);

  // Dispose the Video.js player when the functional component unmounts
  useEffect(() => {
    const player = playerRef.current;

    return () => {
      if (player && !player.isDisposed()) {
        player.dispose();
        playerRef.current = null;
      }
    };
  }, [playerRef]);

  return (
    <div data-vjs-player className="video-js-container">
      <div ref={videoRef} />
    </div>
  );
};

export type VideoPlayerProps = {
  src: string;
  type?: string;
};

const VideoPlayer = ({
  src,
  type = "video/mp4",
}: VideoPlayerProps): JSX.Element => {
  const videoJsOptions = {
    autoplay: false,
    controls: true,
    responsive: true,
    fluid: true,
    preload: "metadata",
    language: translate({
      id: "video.language",
      description: "The language of the video player.",
      message: "en",
    }),
    sources: [
      {
        src: src,
        type: type,
      },
    ],
  };

  return <VideoJS options={videoJsOptions} />;
};

export default VideoPlayer;
