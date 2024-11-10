/**
 * JSON Grid viewer
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-json-grid
 * License: MIT
 *
 * Thanks the base project:
 * https://github.com/RedHeadphone/react-json-grid
 */

import React, {useState, useEffect} from "react";
import clsx from "clsx/lite";

import {useColorMode} from "@docusaurus/theme-common";

import JSONGrid from "@redheadphone/react-json-grid";

import {sanitizeData, sanitizeTheme} from "./utils";
import styles from "./index.module.scss";

type JSONViewProps = {
  data: Object | any[] | number | string | boolean;
  defaultExpandDepth: number;
  defaultExpandKeyTree?: Object;
  theme?:
    | {
        light: string;
        dark: string;
      }
    | string;
};

const JSONView = ({
  data,
  defaultExpandDepth = 2,
  defaultExpandKeyTree,
  theme = {light: "remedy", dark: "moonLight"},
}: JSONViewProps): JSX.Element => {
  const {colorMode, setColorMode} = useColorMode();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div key={String(mounted)}>
      <div className={clsx(styles.jsGridContainer, styles.noSelect)}>
        <JSONGrid
          data={sanitizeData(data)}
          highlightSelected={false}
          theme={sanitizeTheme(theme, colorMode === "dark")}
          defaultExpandDepth={defaultExpandDepth}
          defaultExpandKeyTree={defaultExpandKeyTree}
        />
      </div>
    </div>
  );
};

export default JSONView;
