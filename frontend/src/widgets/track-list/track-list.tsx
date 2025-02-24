import { useState, useEffect } from "react";
import Link from "next/link";
import styles from "./track-list.module.css";

interface TracklistProps {
  name: string;
  name_link: string;
  artist: string;
  artist_link: string;
  favourite: string;
  time: number;
  showRemoveButton: boolean;
  onFavouriteToggle: () => void;
  onRemove?: () => void;
}

export const Tracklist = ({
  name,
  name_link,
  artist,
  artist_link,
  favourite,
  time,
  showRemoveButton,
  onFavouriteToggle,
  onRemove,
}: TracklistProps) => {
  const colorOptions = ["#949E7B", "#B3BF7D", "#758934", "#A1BA65", "#405A01"];
  const [randomColor, setRandomColor] = useState<string>(
    favourite ? colorOptions[0] : "#000"
  );

  useEffect(() => {
    const getRandomColor = (colors: string[]): string => {
      const randomIndex = Math.floor(Math.random() * colors.length);
      return colors[randomIndex];
    };

    setRandomColor(getRandomColor(colorOptions));
  }, []);

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
      2,
      "0"
    )}`;
  };

  return (
    <div className={styles.playlist}>
      <div
        className={styles.playlist__avatar}
        style={{ backgroundColor: randomColor }}
      ></div>

      <div className={styles.playlist__details}>
        <div className={styles.playlist__details__name}>
          <Link href={name_link}>
            <h2 className={styles.playlist__name}>{name}</h2>
          </Link>

          <Link href={artist_link}>
            <p className={styles.playlist__artist}>{artist}</p>
          </Link>
        </div>

        <div className={styles.playlist__favourite} onClick={onFavouriteToggle}>
          {favourite ? (
            <i className="fa-solid fa-star"></i>
          ) : (
            <i className="fa-regular fa-star"></i>
          )}
        </div>

        <div className={styles.playlist__time}>{formatTime(time)}</div>

        {showRemoveButton && onRemove && (
          <div className={styles.playlist__remove} onClick={onRemove}>
            <i className="fa-solid fa-xmark"></i>
          </div>
        )}
      </div>
    </div>
  );
};
