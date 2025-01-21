import styles from "./search-panel.module.css";

export const SearchPanel = () => {
  return (
    <div className={styles.search}>
      <input className={styles.search__input} placeholder="Поиск" />
      <i className={`fa-solid fa-magnifying-glass ${styles.search__icon}`} />
    </div>
  );
};
