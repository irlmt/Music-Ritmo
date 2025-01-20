import { Logo } from "@/shared/logo";
import Link from "next/link";
import { User } from "@/entities/user";

import styles from "./header.module.css";

export const Header = () => {
  return (
    <div className={styles.header}>
      <div className={styles.header__logo}>
        <Logo type="normal" />
      </div>
      <div className={styles.header__buttons}>
        <Link href="/playlists">
          <i className={`fa-solid fa-music ${styles.header__buttons__icons}`} />
        </Link>
        <Link href="/favourite-track">
          <i className={`fa-solid fa-star ${styles.header__buttons__icons}`} />
        </Link>
        <User />
      </div>
    </div>
  );
};
