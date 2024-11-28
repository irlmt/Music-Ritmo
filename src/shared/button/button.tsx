import classNames from "classnames";
import React from "react";

import styles from "./button.module.css";

type ButtonType = "normal" | "transparent";
type ButtonColor = "green" | "white" | "green-text";

interface ButtonProps {
  children?: React.ReactNode;
  className?: string;
  type?: ButtonType;
  color?: ButtonColor;
  onClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className,
  type = "small",
  color = "orange",
  onClick,
  disabled,
}) => {
  const buttonClassName = classNames(className, styles[type], styles[color]);

  return (
    <button className={buttonClassName} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
};
