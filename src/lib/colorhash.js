// An improved alternative:

import {colord, extend} from "colord";
import namesPlugin from "colord/plugins/names";

extend([namesPlugin]);

/**
 * @typedef {[number, number, number, number]} CachedColor - The cached h, s, l, and
 *   fontfg values.
 */

/**
 * cyrb53 (c) 2018 bryc (github.com/bryc)
 *
 * Acquired from https://github.com/bryc/code/blob/master/jshash/experimental/cyrb53.js
 *
 * License: Public domain (or MIT if needed). Attribution appreciated.
 * A fast and simple 53-bit string hash function with decent collision resistance.
 * Largely inspired by MurmurHash2/3, but with a focus on speed/simplicity.
 *
 * @param {string} str - The string to be hashed.
 * @param {number} seed - The random seed used for initializing the hash.
 * @returns {number} - The hash code calculated from `str`.
 */
export const cyrb53 = function (str, seed = 0) {
  let h1 = 0xdeadbeef ^ seed,
    h2 = 0x41c6ce57 ^ seed;
  for (let i = 0, ch; i < str.length; i++) {
    ch = str.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507);
  h1 ^= Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507);
  h2 ^= Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  return 4294967296 * (2097151 & h2) + (h1 >>> 0);
};

/**
 * Convert a hash value to the HSL-FontFG color.
 *
 * @param {number} hash - A hash value solved by a text-to-int algorithm.
 * @returns {CachedColor} The color properties solved from the hash code.
 */
const hashToHSLF = (hash) => {
  const h = hash % 360;
  const l = (hash % 25) + 38;
  return [h, 75, l, hslToY(h, 0.75, l / 100) > 0.55 ? 5 : 95];
};

/**
 * Convert a color-text string to the HSL-FontFG color.
 *
 * @param {string} colorText - A css-like text specifying a color to be converted.
 * @returns {CachedColor} The color properties solved from the text.
 */
const colorTextToHSLF = (colorText) => {
  const hsl = colord(colorText).toHsl();
  return [
    hsl.h,
    hsl.s,
    hsl.l,
    hslToY(hsl.h, hsl.s / 100, hsl.l / 100) > 0.55 ? 5 : 95,
  ];
};

/**
 * Convert HSL color to Y in YUV.
 *
 * Compared to L in HSL, Y is a more reliable metric of the lightness.
 *
 * @param {number} h - H in HSL.
 * @param {number} s - S in HSL.
 * @param {number} l - L in HSL.
 * @param {number} a - Intermediate value. Do not need to configure by users.
 * @param {(n: number, k?: number) => number} f Intermediate calculator. Do not need
 *   to configure by users.
 * @returns {number} - Y value.
 */
export const hslToY = (
  h,
  s,
  l,
  a = s * Math.min(l, 1 - l),
  f = (n, k = (n + h / 30) % 12) =>
    l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
) => (f(0) * 299 + f(8) * 587 + f(4) * 114) / 1000;

/**
 * Calculate the global bounding box color based on a specified color text.
 *
 * @param {string} colorText - The color specified by the text.
 * @param {{
 *   get: (key: string) => CachedColor | null,
 *   put: (key: string, val: CachedColor)
 * }} colorNameCache - The cache of the color name.
 * @returns {{
 *   shapeBackground: string, shapeStrokeStyle: string, shapeShadowStyle: string,
 *   transformerBackground: string, fontBackground: string, fontColor: string
 * } | {}} The dynamic color calculated by the shape data.
 */
export const getGlobalBoxColor = (colorText, colorNameCache) => {
  if (!colorText) {
    return {};
  }
  let cachedColor = colorNameCache?.get && colorNameCache.get(colorText);
  if (cachedColor === null) {
    cachedColor = colorTextToHSLF(colorText);
    if (colorNameCache?.put) {
      colorNameCache.put(colorText, cachedColor);
    }
  }
  if (!cachedColor) {
    return {};
  }
  const [h, s, l, fontfg] = cachedColor;
  return {
    shapeBackground: `hsla(${h}, 16%, 93%, 0.2)`,
    shapeStrokeStyle: `hsl(${h}, ${s}%, ${l}%)`,
    shapeShadowStyle: `hsla(${h}, 9%, 31%, 0.35)`,
    transformerBackground: `hsla(${h}, ${s}%, ${Math.round(0.7 * l)}%)`,
    fontBackground: `hsla(${h}, ${s}%, ${l}%)`,
    fontColor: `hsl(${h}, ${s}%, ${fontfg}%)`,
  };
};

/**
 * Calculate the bounding box color based on the data of a rectangular shape.
 *
 * @param {object} shape - The RectShape object provided by ReactPictureAnnotation.
 * @param {Object.<string, string>} colors - The color dictionary containing the
 *   text-color mapping.
 * @param {{
 *   get: (key: string) => CachedColor | null,
 *   put: (key: string, val: CachedColor)
 * }} hashCache - The cache of the hashCode.
 * @param {{
 *   get: (key: string) => CachedColor | null,
 *   put: (key: string, val: CachedColor)
 * }} colorNameCache - The cache of the color name.
 * @param {bool} useHash - Whether to use hash to dynamically generate colors.
 * @returns {{
 *   shapeBackground: string, shapeStrokeStyle: string, shapeShadowStyle: string,
 *   transformerBackground: string, fontBackground: string, fontColor: string
 * } | {}} The dynamic color calculated by the shape data.
 */
export const getBoxColor = (
  shape,
  colors,
  hashCache,
  colorNameCache,
  useHash
) => {
  const comment = shape?.annotationData?.comment;
  if (!comment) {
    return {};
  }
  // Get the color by the name;
  const colorText = colors ? colors[comment] : undefined;
  let cachedColor = undefined;
  if (colorText) {
    cachedColor = colorNameCache?.get && colorNameCache.get(colorText);
    if (cachedColor === null) {
      cachedColor = colorTextToHSLF(colorText);
      if (colorNameCache?.put) {
        colorNameCache.put(colorText, cachedColor);
      }
    }
  }
  // Get the color by hash;
  if (useHash && !cachedColor) {
    cachedColor = hashCache?.get && hashCache.get(comment);
    if (cachedColor == null) {
      cachedColor = hashToHSLF(cyrb53(comment, 1023));
      if (hashCache?.put) {
        hashCache.put(comment, cachedColor);
      }
    }
  }
  if (!cachedColor) {
    return {};
  }
  const [h, s, l, fontfg] = cachedColor;
  return {
    shapeBackground: `hsla(${h}, 16%, 93%, 0.2)`,
    shapeStrokeStyle: `hsl(${h}, ${s}%, ${l}%)`,
    shapeShadowStyle: `hsla(${h}, 9%, 31%, 0.35)`,
    transformerBackground: `hsla(${h}, ${s}%, ${Math.round(0.7 * l)}%)`,
    fontBackground: `hsla(${h}, ${s}%, ${l}%)`,
    fontColor: `hsl(${h}, ${s}%, ${fontfg}%)`,
  };
};
