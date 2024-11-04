import React from "react";
import IconDelete from "../icons/delete";

/**
 * Input component.
 *
 * Acquired and modified from
 * https://github.com/Kunduin/react-picture-annotation/blob/master/src/DefaultInputSection.tsx
 *
 * @param {object} props - The input properties.
 * @param {string} props.value - The value of the input component.
 * @param {(value: string) => void} props.onChange - The callback fired when the values
 *   are changed.
 * @param {() => void} props.onDelete - The callback fired when the delete button is
 *   clicked.
 * @param {string} props.placeholder - The placeholder if the item is empty.
 * @returns
 */
const Input = ({value, onChange, onDelete, placeholder = "Input tag here"}) => {
  return (
    <div className="rp-default-input-section">
      <input
        className="rp-default-input-section_input"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      <a
        className="rp-default-input-section_delete"
        style={{color: "white"}}
        onClick={() => onDelete()}
      >
        <IconDelete />
      </a>
    </div>
  );
};

export default Input;
