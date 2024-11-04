import React from "react";

export const DashPictureAnnotation = React.lazy(() =>
  import(
    /* webpackChunkName: "DashPictureAnnotation" */ "./fragments/DashPictureAnnotation.react"
  )
);
