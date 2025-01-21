"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import styles from "./user.module.css";

export const User = () => {
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen((prevState) => !prevState);
  };

  return (
    <div className={styles.user}>
      <div className={styles.user__avatar} onClick={toggleMenu}>
        <Image
          src="/images/logo.svg"
          alt="User Avatar"
          width={40}
          height={40}
          className={styles.user__avatar__image}
        />
        <span className={styles.user__avatar__name}>Иванов Иван</span>
      </div>

      {isMenuOpen && (
        <div className={styles.user__menu}>
          <ul className={styles.user__menu_list}>
            <li>
              <Link href="/settings" className={styles.user__menu_item}>
                Настройки
              </Link>
            </li>
            <li>
              <Link href="/login" className={styles.user__menu_item}>
                Выйти
              </Link>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
};
