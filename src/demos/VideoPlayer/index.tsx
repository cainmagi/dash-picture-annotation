/**
 * Videos used in the project.
 * Yuchen Jin, mailto:cainmagi@gmail.com
 */

import Plyr from "plyr-react";
import "./VideoPlayer.css";

import {translate} from "@docusaurus/Translate";

type VideoPlayerProps = {
  src: string;
  type: string;
  options: {
    enabled?: boolean;
    settings?: ["captions"?, "quality"?, "speed"?, "loop"?];
    autoplay?: boolean;
  };
};

const getLocalization = () => {
  const qualityBadge = {};
  Object.entries({
    2160: "4K",
    1440: "HD",
    1080: "HD",
    720: "HD",
    576: "SD",
    480: "SD",
  }).forEach(([key, value]) => {
    qualityBadge[key] = translate({
      id: `videos.qualityBadge.${key}`,
      description: `The translation for the video component: ${value}`,
      message: value,
    });
  });

  return {
    restart: translate({
      id: "videos.restart",
      description: "The translation for the video component: Restart",
      message: "Restart",
    }),
    rewind: translate(
      {
        id: "videos.rewind",
        description:
          "The translation for the video component: Rewind {seektime}s",
        message: "Rewind {seektime}s",
      },
      {seektime: "{seektime}"}
    ),
    play: translate({
      id: "videos.play",
      description: "The translation for the video component: Play",
      message: "Play",
    }),
    pause: translate({
      id: "videos.pause",
      description: "The translation for the video component: Pause",
      message: "Pause",
    }),
    fastForward: translate(
      {
        id: "videos.fastForward",
        description:
          "The translation for the video component: Forward {seektime}s",
        message: "Forward {seektime}s",
      },
      {seektime: "{seektime}"}
    ),
    seek: translate({
      id: "videos.seek",
      description: "The translation for the video component: Seek",
      message: "Seek",
    }),
    seekLabel: translate(
      {
        id: "videos.seekLabel",
        description:
          "The translation for the video component: {currentTime} of {duration}",
        message: "{currentTime} of {duration}",
      },
      {currentTime: "{currentTime}", duration: "{duration}"}
    ),
    played: translate({
      id: "videos.played",
      description: "The translation for the video component: Played",
      message: "Played",
    }),
    buffered: translate({
      id: "videos.buffered",
      description: "The translation for the video component: Buffered",
      message: "Buffered",
    }),
    currentTime: translate({
      id: "videos.currentTime",
      description: "The translation for the video component: Current time",
      message: "Current time",
    }),
    duration: translate({
      id: "videos.duration",
      description: "The translation for the video component: Duration",
      message: "Duration",
    }),
    volume: translate({
      id: "videos.volume",
      description: "The translation for the video component: Volume",
      message: "Volume",
    }),
    mute: translate({
      id: "videos.mute",
      description: "The translation for the video component: Mute",
      message: "Mute",
    }),
    unmute: translate({
      id: "videos.unmute",
      description: "The translation for the video component: Unmute",
      message: "Unmute",
    }),
    enableCaptions: translate({
      id: "videos.enableCaptions",
      description: "The translation for the video component: Enable captions",
      message: "Enable captions",
    }),
    disableCaptions: translate({
      id: "videos.disableCaptions",
      description: "The translation for the video component: Disable captions",
      message: "Disable captions",
    }),
    download: translate({
      id: "videos.download",
      description: "The translation for the video component: Download",
      message: "Download",
    }),
    enterFullscreen: translate({
      id: "videos.enterFullscreen",
      description: "The translation for the video component: Enter fullscreen",
      message: "Enter fullscreen",
    }),
    exitFullscreen: translate({
      id: "videos.exitFullscreen",
      description: "The translation for the video component: Exit fullscreen",
      message: "Exit fullscreen",
    }),
    frameTitle: translate(
      {
        id: "videos.frameTitle",
        description:
          "The translation for the video component: Player for {title}",
        message: "Player for {title}",
      },
      {title: "{title}"}
    ),
    captions: translate({
      id: "videos.captions",
      description: "The translation for the video component: Captions",
      message: "Captions",
    }),
    settings: translate({
      id: "videos.settings",
      description: "The translation for the video component: Settings",
      message: "Settings",
    }),
    pip: translate({
      id: "videos.pip",
      description: "The translation for the video component: PIP",
      message: "PIP",
    }),
    menuBack: translate({
      id: "videos.menuBack",
      description:
        "The translation for the video component: Go back to previous menu",
      message: "Go back to previous menu",
    }),
    speed: translate({
      id: "videos.speed",
      description: "The translation for the video component: Speed",
      message: "Speed",
    }),
    normal: translate({
      id: "videos.normal",
      description: "The translation for the video component: Normal",
      message: "Normal",
    }),
    quality: translate({
      id: "videos.quality",
      description: "The translation for the video component: Quality",
      message: "Quality",
    }),
    loop: translate({
      id: "videos.loop",
      description: "The translation for the video component: Loop",
      message: "Loop",
    }),
    start: translate({
      id: "videos.start",
      description: "The translation for the video component: Start",
      message: "Start",
    }),
    end: translate({
      id: "videos.end",
      description: "The translation for the video component: End",
      message: "End",
    }),
    all: translate({
      id: "videos.all",
      description: "The translation for the video component: All",
      message: "All",
    }),
    reset: translate({
      id: "videos.reset",
      description: "The translation for the video component: Reset",
      message: "Reset",
    }),
    disabled: translate({
      id: "videos.disabled",
      description: "The translation for the video component: Disabled",
      message: "Disabled",
    }),
    enabled: translate({
      id: "videos.enabled",
      description: "The translation for the video component: Enabled",
      message: "Enabled",
    }),
    advertisement: translate({
      id: "videos.advertisement",
      description: "The translation for the video component: Ad",
      message: "Ad",
    }),
    qualityBadge: {
      2160: translate({
        id: "videos.qualityBadge.2160",
        description: "The translation for the video component: 4K",
        message: "4K",
      }),
      1440: translate({
        id: "videos.qualityBadge.1440",
        description: "The translation for the video component: HD",
        message: "HD",
      }),
      1080: translate({
        id: "videos.qualityBadge.1080",
        description: "The translation for the video component: HD",
        message: "HD",
      }),
      720: translate({
        id: "videos.qualityBadge.720",
        description: "The translation for the video component: HD",
        message: "HD",
      }),
      576: translate({
        id: "videos.qualityBadge.576",
        description: "The translation for the video component: SD",
        message: "SD",
      }),
      480: translate({
        id: "videos.qualityBadge.480",
        description: "The translation for the video component: SD",
        message: "SD",
      }),
    },
  };
};

const VideoPlayer = ({
  src,
  type = "video/mp4",
  options,
}: VideoPlayerProps): JSX.Element => {
  const source: Plyr.SourceInfo = {
    type: "video",
    title: "Example title",
    sources: [
      {
        src: src,
        type: type,
        size: 1080,
      },
    ],
  };
  return (
    <Plyr source={source} options={{i18n: getLocalization(), ...options}} />
  );
};

export default VideoPlayer;
