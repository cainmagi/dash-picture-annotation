/**
 * Utilities
 *
 * The utilities used by other components.
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-picture-annotation
 * License: MIT
 *
 * Thanks the base project:
 * https://github.com/Kunduin/react-picture-annotation
 */

import {type, hasIn, max} from "ramda";

export const isArray =
  Array.isArray ||
  ((value) => {
    return value instanceof Array;
  });

/**
 * Sanitize a value `val` and ensures that it is not smaller than another value
 * `minVal`.
 *
 * @param {number} val - The value to be sanitized.
 * @param {number} minVal - The lower boundary that `val` should have.
 * @returns {number} - The sanitized `val` not smaller than `minVal`.
 */
export const requireMin = (val, minVal = 0) => {
  if (type(val) === "Number") {
    return max(val, minVal);
  }
  return minVal;
};

/**
 * Sanitize scale
 * @param {number|object} scale - The scale factor to be sanitized
 * @returns {{scale: number, offset_x: number, offset_y: number}} - An array of sanitized options
 */
export const sanitizeScale = (scale) => {
  if (type(scale) === "Object") {
    return {
      scale:
        hasIn("scale", scale) && type(scale.scale) === "Number"
          ? scale.scale
          : 1.0,
      offset_x:
        hasIn("offset_x", scale) && type(scale.offset_x) === "Number"
          ? scale.offset_x
          : 0.5,
      offset_y:
        hasIn("offset_y", scale) && type(scale.offset_y) === "Number"
          ? scale.offset_y
          : 0.5,
    };
  }
  if (type(scale) === "Number") {
    return {
      scale: scale,
      offset_x: 0.5,
      offset_y: 0.5,
    };
  }
  return {
    scale: 1.0,
    offset_x: 0.5,
    offset_y: 0.5,
  };
};

/**
 * Sanitize options
 * Copied from
 * https://github.com/plotly/dash/blob/dev/components/dash-core-components/src/utils/optionTypes.js
 * @param {array|object} options - The options to be sanitized
 * @returns {{label: string, value: string}[]} - An array of sanitized options
 */
export const sanitizeOptions = (options) => {
  if (type(options) === "Object") {
    return Object.entries(options).map(([value, label]) => ({
      label: React.isValidElement(label) ? label : String(label),
      value,
    }));
  }

  if (type(options) === "Array") {
    if (
      options.length > 0 &&
      ["String", "Number", "Bool"].includes(type(options[0]))
    ) {
      return options.map((option) => ({
        label: String(option),
        value: option,
      }));
    }
    return options;
  }

  return options;
};

/**
 * randomID
 * Copied from https://github.com/Kunduin/react-picture-annotation/blob/master/src/utils/randomId.ts
 * @param {number} len - The length of the random ID
 * @returns {string} - The synthesized random ID
 */
export const randomID = (len = 6) => {
  const chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678";
  const maxPos = chars.length;
  let id = "";
  for (let i = 0; i < len; i++) {
    id += chars.charAt(Math.floor(Math.random() * maxPos));
  }
  return id;
};

/**
 * Sanitize data
 *
 * @param {array|object|null|undefined} data - The data to be sanitized
 * @returns {{
 *   timestamp: number,
 *   data: {
 *     id: string,
 *     mark: {x: number, y: number, width: number, height: number, type: "RECT"},
 *     comment?: string
 *   }[]
 * }} - An array of sanitized data
 */
export const sanitizeData = (data) => {
  if (type(data) === "Undefined" || type(data) === "Null") {
    return {
      timestamp: Date.now(),
      data: [],
    };
  }

  let dataArray = [];
  let timestamp = Date.now();
  if (type(data) === "Array") {
    dataArray = data;
  }
  if (type(data) === "Object") {
    if (hasIn("data", data)) {
      dataArray = data.data;
    }
    if (hasIn("timestamp", data) && type(data.timestamp) === "Number") {
      timestamp = data.timestamp;
    }
  }

  dataArray = dataArray.reduce((results, {id, mark, comment}) => {
    if (type(mark) === "Undefined") {
      return results;
    }
    let ditem = {
      id: type(id) === "String" ? id : randomID(),
      mark: mark,
    };
    if (type(comment) === "String") {
      ditem.comment = comment;
    }
    results.push(ditem);
    return results;
  }, []);

  return {
    timestamp: timestamp,
    data: dataArray,
  };
};

/**
 * Sanitize data (faster version)
 * This method does not check the deep part of the data. It should be faster.
 *
 * @param {array|object|null|undefined} data - The data to be sanitized
 * @returns {{
 *   timestamp: number,
 *   data: {
 *     id: string,
 *     mark: {x: number, y: number, width: number, height: number, type: "RECT"},
 *     comment?: string
 *   }[]
 * }} - An array of sanitized data
 */
export const sanitizeDataFast = (data) => {
  if (type(data) === "Undefined" || type(data) === "Null") {
    return {
      timestamp: Date.now(),
      data: [],
    };
  }

  let dataArray = [];
  let timestamp = Date.now();
  if (type(data) === "Array") {
    dataArray = data;
  }
  if (type(data) === "Object") {
    if (hasIn("data", data)) {
      dataArray = data.data;
    }
    if (hasIn("timestamp", data) && type(data.timestamp) === "Number") {
      timestamp = data.timestamp;
    }
  }

  return {
    timestamp: timestamp,
    data: dataArray,
  };
};
