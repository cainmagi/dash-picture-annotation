/* eslint no-magic-numbers: 0 */
import React, {useState} from "react";

import {DashPictureAnnotation} from "../lib";

const App = () => {
  const [state, setState] = useState({
    image: "https://upload.wikimedia.org/wikipedia/commons/b/bd/Test.svg",
    disabled: false,
    is_color_dynamic: false,
    size_minimal: {
      width: 5,
      height: 5,
    },
    colors: {},
    options: [
      {value: "Title", label: "Title"},
      {value: "Label", label: "Label"},
    ],
  });

  const [data, setData] = useState({
    timestamp: Date.now(),
    data: [
      {
        id: "AYAder",
        mark: {
          x: 200.87731048580005,
          y: 78.57834993258817,
          width: 196.74579219762532,
          height: 198.54529639455487,
          type: "RECT",
        },
        comment: "Title",
      },
    ],
  });

  const setProps = (newProps) => {
    console.log("newprops:", newProps);
    if (Object.prototype.hasOwnProperty.call(newProps, "data")) {
      setData(newProps.data);
      delete newProps.data;
    }
    setState(Object.assign({}, state, newProps));
  };

  const handleOnClick = () => {
    if (state.image.endsWith("Test.svg")) {
      setProps({
        image:
          "https://upload.wikimedia.org/wikipedia/commons/a/aa/Philips_PM5544.svg",
      });
    } else {
      setProps({
        image: "https://upload.wikimedia.org/wikipedia/commons/b/bd/Test.svg",
      });
    }
  };

  const handleChangeData = () => {
    setData({
      timestamp: Date.now(),
      data: [
        {
          id: "AYAder",
          mark: {
            x: 25.87731048580005,
            y: 25.57834993258817,
            width: 196.74579219762532,
            height: 198.54529639455487,
            type: "RECT",
          },
          comment: "VASS",
        },
        {
          id: "bjg",
          mark: {
            x: 99.87731048580005,
            y: 99.57834993258817,
            width: 88.74579219762532,
            height: 88.54529639455487,
            type: "RECT",
          },
          comment: "VASK",
        },
        {
          id: "adf",
          mark: {
            x: 199.87731048580005,
            y: 199.57834993258817,
            width: 88.74579219762532,
            height: 88.54529639455487,
            type: "RECT",
          },
          comment: "TEST",
        },
      ],
    });
  };

  const handleChangeStyle = () => {
    const style_annotations = [
      "#444",
      "#AAA",
      "#BB9",
      {
        shapeStrokeStyle: "#000000",
      },
    ];
    setProps({
      style_annotation: style_annotations[Math.floor(Math.random() * 4)],
    });
  };

  const handleDisabled = () => {
    const disabled = state.disabled;
    setProps({disabled: disabled ? false : true});
  };

  const handleColorDynamic = () => {
    const is_color_dynamic = state.is_color_dynamic;
    setProps({is_color_dynamic: is_color_dynamic ? false : true});
  };

  const handleColorChange = () => {
    const clrs = ["red", "yellow", "green", "#888888"];
    setProps({colors: {TEST: clrs[Math.floor(Math.random() * 4)]}});
  };

  const handleOptions = () => {
    const curOptions = state.options;
    if (curOptions) {
      setProps({options: undefined});
    } else {
      setProps({
        options: [
          {value: "Title", label: "Title"},
          {value: "Label", label: "Label"},
        ],
      });
    }
  };

  return (
    <div>
      <DashPictureAnnotation
        setProps={setProps}
        data={data}
        style={{height: "80vh", marginBottom: "1rem"}}
        placeholder_dropdown={"test2"}
        placeholder_input={"test1"}
        {...state}
      />
      <p>
        <button onClick={handleOnClick} style={{marginRight: "1rem"}}>
          Refresh Image
        </button>
        <button onClick={handleChangeData} style={{marginRight: "1rem"}}>
          Refresh Data
        </button>
        <button onClick={handleChangeStyle} style={{marginRight: "1rem"}}>
          Change Style
        </button>
        <button onClick={handleDisabled} style={{marginRight: "1rem"}}>
          Toggle disabled
        </button>
        <button onClick={handleColorDynamic} style={{marginRight: "1rem"}}>
          Toggle color dynamic
        </button>
        <button onClick={handleOptions} style={{marginRight: "1rem"}}>
          Toggle options
        </button>
        <button onClick={handleColorChange}>Change color for "TEST"</button>
      </p>
      <p>{JSON.stringify(data)}</p>
    </div>
  );
};

export default App;
