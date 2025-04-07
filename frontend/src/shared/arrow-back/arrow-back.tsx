import React from "react";
import Link from "next/link";
import styles from "./arrow-back.module.css";
import { useRouter } from "next/navigation";

interface arrowBackProps {
  className?: string;
  link?: string;
}

export const ArrowBack: React.FC<arrowBackProps> = ({
  className,
  link = "/",
}) => {
  const router = useRouter();
  const handleBackClick = () => {
    router.back();
  };

  return (
    <Link
      href={link}
      className={className}
      data-testid="arrow-back"
      onClick={handleBackClick}
    >
      <i
        className={`fa-solid fa-arrow-left ${styles.arrow}`}
        role="img"
        aria-label="Back"
      />
    </Link>
  );
};
