import React from "react";

import styles from "./arrow-back.module.css";

interface arrowBackProps {
  className?: string;
  link?: string;
}

export const ArrowBack: React.FC<arrowBackProps> = ({ className, link }) => {
  return (
    <a href={link} className={className}>
      <i className={`fa-solid fa-arrow-left ${styles.arrow}`} />
    </a>
  );
};
