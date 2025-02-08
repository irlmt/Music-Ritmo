import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useAuth } from "@/app/auth-context";
import styles from "./user.module.css";

export const User = () => {
  const { user, logout } = useAuth();
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen((prevState) => !prevState);
  };

  const handleLogout = () => {
    logout();
    setMenuOpen(false);
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
        <span className={styles.user__avatar__name}>{user}</span>
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
              <button className={styles.user__menu_item} onClick={handleLogout}>
                Выйти
              </button>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
};
