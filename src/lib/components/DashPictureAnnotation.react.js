import React from "react";
import PropTypes from "prop-types";
import {DashPictureAnnotation as RealComponent} from "../LazyLoader";

/**
 * DashPictureAnnotation is a Dash porting version for the React component:
 * `react-picture-annotation/ReactPictureAnnotation`.
 *
 * This component provides a annotator that allows users to create, modify, or delete
 * the annotation information for a specific picture. This dash version has been
 * upgraded by adding the following features:
 * 1. Responsive size with respect to the parent component.
 * 2. Annotation type specified by a selector rather than an input box.
 * 3. Only trigger the data update when the mouse is released.
 * 4. Extensive functionalities for fine-grained customization of colors.
 * 5. Disabling the annotator by a flag.
 * 6. Setting a lower boundary of the annotation size to prevent small annotations
 *    created by mistake.
 */
const DashPictureAnnotation = (props) => {
  return (
    <React.Suspense fallback={null}>
      <RealComponent {...props} />
    </React.Suspense>
  );
};

DashPictureAnnotation.defaultProps = {
  style: {height: "60vh"},
  placeholder_input: "Input tag here",
  placeholder_dropdown: "Select a tag",
  clearable_dropdown: false,
  disabled: false,
  is_color_dynamic: false,
  size_minimal: {
    width: 0,
    height: 0,
  },
};

DashPictureAnnotation.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: PropTypes.string,

  /**
   * The css-class of the component. Use ` ` to separate different names. Often used
   * with CSS to style elements with common properties.
   */
  class_name: PropTypes.string,

  /**
   * The css-styles which will override styles of the component container.
   */
  style: PropTypes.object,

  /**
   * The css-styles of the annotation marker (box).
   * If this value is specified as a string, the string will be parsed as the default
   * color of the annotation boxes.
   */
  style_annotation: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.shape({
      /**
       * Shape style: text padding.
       */
      padding: PropTypes.number,

      /**
       * Shape style: text font size.
       */
      fontSize: PropTypes.number,

      /**
       * Shape style: text font color.
       */
      fontColor: PropTypes.string,

      /**
       * Shape style: text background color.
       */
      fontBackground: PropTypes.string,

      /**
       * Shape style: text font name.
       */
      fontFamily: PropTypes.string,

      /**
       * Shape style: stroke width.
       */
      lineWidth: PropTypes.number,

      /**
       * Shape style: background color in the middle of the marker.
       */
      shapeBackground: PropTypes.string,

      /**
       * Shape style: shape stroke color.
       */
      shapeStrokeStyle: PropTypes.string,

      /**
       * Shape style: stroke shadow blur.
       */
      shadowBlur: PropTypes.number,

      /**
       * Shape style: shape shadow color.
       */
      shapeShadowStyle: PropTypes.string,

      /**
       * Shape style: color of the scalable dots around the selected box.
       */
      transformerBackground: PropTypes.string,

      /**
       * Shape style: size of the scalable dots around the selected box.
       */
      transformerSize: PropTypes.number,
    }),
  ]),

  /**
   * A dictionary of colors. The keys and the values represent the annotation name
   * (specified by the `comment` property of `data`) and the color string,
   * respectively.
   * This method is used for specifying the annotation colors manually. It has a
   * higher priority compared to `is_color_dynamic`.
   */
  colors: PropTypes.objectOf(PropTypes.string),

  /**
   * The URL to the image to be currently displayed on the annotator. The usage is
   * similar to the property of the HTML image tag: `<img src={...}>`.
   */
  image: PropTypes.string,

  /**
   * The annotation data. This value is a sequence of annotation items. Each item
   * contain the positional information and the annotation comment (the object type).
   * This value will can be updated by callbacks or user operations on the annotator.
   */
  data: PropTypes.exact({
    /**
     * The time stamp of the current data.
     * This value is used for identify the version of the data. It can also notify
     * dash that the callback should be fired when this value changes.
     */
    timestamp: PropTypes.number,

    /**
     * The body of the data. Returned from the React annotation data.
     */
    data: PropTypes.arrayOf(
      PropTypes.shape({
        /**
         * The ID of the annotation item. It is only used for locating which annotation
         * item is selected by users.
         */
        id: PropTypes.string,
        /**
         * The bounding box information of the annotation item.
         */
        mark: PropTypes.exact({
          /**
           * The X (horizontal) position of the upper left corner.
           */
          x: PropTypes.number,
          /**
           * The Y (vertical) position of the upper left corner.
           */
          y: PropTypes.number,
          /**
           * The width of the annotation item.
           */
          width: PropTypes.number,
          /**
           * The height of the annotation item.
           */
          height: PropTypes.number,
          /**
           * The shape of the annotation item. Currently, we only support "RECT".
           */
          type: PropTypes.oneOf(["RECT"]),
        }),
        /**
         * The text comment on this annotation item. Typically, this value is specified
         * by the type of the label.
         */
        comment: PropTypes.string,
      })
    ),
  }),

  /**
   * The available options of the annotator. The usage is like the selector component
   * `dcc.Dropdown(options=...)`. Each item represents an available choice of the
   * annotation type.
   * If this value is empty, will use a input box that allows users to specify any
   * type names.
   */
  options: PropTypes.oneOfType([
    PropTypes.arrayOf(
      PropTypes.exact({
        /**
         * Label (displayed text) of the option.
         */
        label: PropTypes.string.isRequired,
        /**
         * The value of the option which will be applied to the annotation data.
         */
        value: PropTypes.any.isRequired,
        /**
         * A flag. If specified, this option item will be not selectable.
         */
        disabled: PropTypes.bool,
      })
    ),
    PropTypes.arrayOf(
      PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.bool])
    ),
    PropTypes.object,
    PropTypes.oneOf([null]),
  ]),

  /**
   * The ID of the currently selected annotation.
   * This property is read-only. It will be automatically set when users select an
   * annotation. A valid ID is a string. When no annotation is selected, this property
   * returns `None`.
   */
  selected_id: PropTypes.oneOfType([PropTypes.string, PropTypes.oneOf([null])]),

  /**
   * The placeholder text when the editor is the input box (the property `options` is
   * empty).
   */
  placeholder_input: PropTypes.string,

  /**
   * The placeholder text when the editor is the dropdown component (the property
   * `options` contains valid items).
   */
  placeholder_dropdown: PropTypes.string,

  /**
   * A flag. Set it to allow the annotation comment to be cleared when the dropdown
   * box is being used.
   */
  clearable_dropdown: PropTypes.bool,

  /**
   * A flag for disabling the annotator (make unclickable).
   */
  disabled: PropTypes.bool,

  /**
   * A flag. If this flag is turned on, will make the color of each annotation box
   * dynamically calculated based on the text of the annotation. An annotation box
   * without a text comment will not be influenced.
   */
  is_color_dynamic: PropTypes.bool,

  /**
   * The requirement of the minimal annotation size. Any newly created annotation with
   * a size smaller than this size will be dropped.
   * If this value is configured as a scalar, will use it for both `width` and `height`.
   * If any of the value is not set or configured as invalid values, will use `0`.
   */
  size_minimal: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.shape({
      /**
       * Requirement of the minimal width of an annotation.
       */
      width: PropTypes.number,
      /**
       * Requirement of the minimal height of an annotation.
       */
      height: PropTypes.number,
    }),
  ]),

  /**
   * Object that holds the loading state object coming from dash-renderer.
   */
  loading_state: PropTypes.shape({
    /**
     * Determines if the component is loading or not
     */
    is_loading: PropTypes.bool,
    /**
     * Holds which property is loading
     */
    prop_name: PropTypes.string,
    /**
     * Holds the name of the component that is loading
     */
    component_name: PropTypes.string,
  }),

  /**
   * Dash-assigned callback that should be called to report property changes
   * to Dash, to make them available for callbacks.
   */
  setProps: PropTypes.func,
};

export default DashPictureAnnotation;

export const defaultProps = DashPictureAnnotation.defaultProps;
export const propTypes = DashPictureAnnotation.propTypes;
