/**
 * Environmental variables of this side.
 * Yuchen Jin, mailto:cainmagi@gmail.com
 */

import React from "react";
import Link from "@docusaurus/Link";
import {useDocsPreferredVersion} from "@docusaurus/theme-common";
import IconExternalLink from "@theme/Icon/ExternalLink";

import InlineIcon from "../components/InlineIcon";
import mdiDot from "@iconify-icons/mdi/dot";
import {biSlashLg} from "../components/icons/BiSlashLg";

const docsPluginId = undefined; // Default docs plugin instance

const variables = {
  repoURL: "https://github.com/cainmagi/dash-picture-annotation",
  rawURL: "https://raw.githubusercontent.com/cainmagi/dash-picture-annotation",
  sourceVersion: {
    main: "main",
  },
  dependencyVersion: {
    main: "1.2.0",
  },
  sourceURIs: {
    main: {
      ".": "__init__.py",
      DashPictureAnnotation: "__init__.py#L30",
      typehints: "typehints.py",
      "typehints.AnnoMark": "typehints.py#L50",
      "typehints.AnnoItem": "typehints.py#L88",
      "typehints.Annotations": "typehints.py#L111",
      "typehints.AnnoStyle": "typehints.py#L124",
      "typehints.DashSelectOptionItem": "typehints.py#L181",
      "typehints.Size": "typehints.py#L193",
      "typehints.NSAnnoItem": "typehints.py#L209",
      "typehints.NSAnnotations": "typehints.py#L224",
      "typehints.is_sequence_of": "typehints.py#L228",
      "typehints.is_anno_mark": "typehints.py#L244",
      "typehints.is_anno_item": "typehints.py#L256",
      "typehints.is_annotations": "typehints.py#L270",
      "typehints.is_dash_select_option_item": "typehints.py#L286",
      utilities: "utilities.py",
      "utilities.get_data_item": "utilities.py#L57",
      "utilities.get_data_item_with_default": "utilities.py#L84",
      "utilities.get_data_items": "utilities.py#L128",
      "utilities.get_data_items_by_regex": "utilities.py#L184",
      "utilities.get_all_ids": "utilities.py#L254",
      "utilities.get_all_comments": "utilities.py#L283",
      "utilities.compare_anno_marks": "utilities.py#L317",
      "utilities.sanitize_data_item": "utilities.py#L412",
      "utilities.sanitize_data": "utilities.py#L487",
    },
  },
};

const useCurrentSourceVersion = (): string => {
  const versionHook: any = useDocsPreferredVersion(docsPluginId);
  const versionLabel = versionHook?.preferredVersion?.label;
  return (
    variables.sourceVersion[versionLabel] || variables.sourceVersion["main"]
  );
};

export type DependencyTagProps = {
  ver: string;
};

export const DependencyTag = ({
  ver = "main",
}: DependencyTagProps): JSX.Element => {
  const _ver = ver?.toLowerCase() === "next" ? "main" : ver;
  const versionDeps = variables.dependencyVersion[_ver];
  return versionDeps ? (
    <Link
      href={`https://github.com/Kunduin/react-picture-annotation/tree/v${versionDeps}`}
    >
      <code>{`react-picture-annotation@${versionDeps}`}</code>
      <IconExternalLink />
    </Link>
  ) : (
    <InlineIcon icon={biSlashLg} />
  );
};

export const rawURL = (url: string): string => {
  return variables.rawURL + "/" + url;
};

export const repoURL = (url: string | undefined = undefined): string => {
  return url ? variables.repoURL + "/" + url : variables.repoURL;
};

export const releaseURL = (ver: string | undefined = undefined): string => {
  const _ver = ver?.toLowerCase() === "next" ? "main" : ver;
  const version = variables.sourceVersion[_ver] || useCurrentSourceVersion();
  if (version === "main" || _ver === "main") {
    return variables.repoURL + "/releases/latest";
  }
  return variables.repoURL + "/releases/tag/" + version;
};

export const rootURL = (url: string): string => {
  const currentSourceVersion = useCurrentSourceVersion();
  return variables.repoURL + "/blob/" + currentSourceVersion + "/" + url;
};

const getURIByVersionPath = (path: string, ver: string): string => {
  const routes = typeof path === "string" ? path.trim() : "";
  if (routes.length === 0) {
    return path;
  }
  const currentURI = variables.sourceURIs[ver] || variables.sourceURIs["main"];
  return currentURI[path] || path;
};

export const sourceURL = (url: string): string => {
  const currentSourceVersion = useCurrentSourceVersion();
  return (
    variables.repoURL +
    "/blob/" +
    currentSourceVersion +
    "/dash_picture_annotation/" +
    getURIByVersionPath(url, currentSourceVersion)
  );
};

export const demoURL = (url?: string): string => {
  const currentSourceVersion = useCurrentSourceVersion();
  if (!url) {
    return variables.repoURL + "/blob/" + currentSourceVersion + "/usage.py";
  }
  return (
    variables.repoURL + "/blob/" + currentSourceVersion + "/examples/" + url
  );
};

export type SourceLinkProps = {
  url: string;
  children: React.ReactNode;
};

export const SourceLink = ({url, children}: SourceLinkProps): JSX.Element => {
  return (
    <Link to={sourceURL(url)} className="noline">
      {children}
    </Link>
  );
};

export type SplitterProps = {
  padx?: string;
};

export const Splitter = ({padx = "0"}: SplitterProps): JSX.Element => {
  return (
    <span style={{padding: "0 " + padx}}>
      <InlineIcon icon={mdiDot} />
    </span>
  );
};
