import classNames from "classnames";
import React from "react";

import styles from "./container.module.css";

type directionType = "row" | "column";

interface ContainerProps {
  children?: React.ReactNode;
  style?: React.CSSProperties;
  direction?: directionType;
}

export const Container: React.FC<ContainerProps> = ({
  children,
  style,
  direction = "column",
}) => {
  const containerClassName = classNames(styles.container, styles[direction]);

  return (
    <div className={containerClassName} style={style}>
      {children}
    </div>
  );
};
