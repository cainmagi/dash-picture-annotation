import React, {Component} from "react";
import clsx from "clsx";
import disableScroll from "disable-scroll";

import Select, {components} from "react-select";

import IconDelete from "../icons/delete";
import styles from "./Dropdown.module.css";

const EnableScrollMenu = ({children, ...props}) => {
  return (
    <div
      onMouseEnter={(e) => {
        disableScroll.off();
      }}
      onMouseLeave={(e) => {
        disableScroll.off();
      }}
    >
      <components.Menu captureMenuScroll {...props}>
        {children}
      </components.Menu>
    </div>
  );
};

/**
 * Dropdown powered by react-select:
 * This sub-component is used for customizing the annotation type among the names
 * specified by users.
 */
export default class Dropdown extends Component {
  constructor(props) {
    super(props);
    this.getCurValue = this.getCurValue.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.onDelete = this.onDelete.bind(this);
  }

  getCurValue() {
    const value = this.props.value;
    if (!value) {
      return null;
    }
    const options = this.props.options;
    if (!options) {
      return null;
    }
    const newValue = options.find((element) => element.value === value);
    return newValue ? newValue : null;
  }

  handleChange(e) {
    const {onChange} = this.props;
    const v = e?.value;
    onChange(v);
  }

  onDelete() {
    const {onDelete} = this.props;
    onDelete();
  }

  render() {
    return (
      <div className={clsx(styles["dropdown"], styles.row)}>
        <div className={styles["col-main"]}>
          <Select
            value={this.getCurValue()}
            onChange={this.handleChange}
            options={this.props.options}
            components={{Menu: EnableScrollMenu}}
            placeholder={this.props.placeholder}
            isClearable={this.props.isClearable}
            isOptionDisabled={(option) => {
              return option?.disabled === true;
            }}
          />
        </div>
        <div className={clsx(styles["btn-delete"], styles["col-btn"])}>
          <a className={styles["icon-delete"]} onClick={this.onDelete}>
            <IconDelete />
          </a>
        </div>
      </div>
    );
  }
}
