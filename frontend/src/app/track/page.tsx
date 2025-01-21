"use client";

import { useState, useEffect } from "react";
import { Container } from "@/shared/container";
import Link from "next/link";
import styles from "./track.module.css";

export default function PlayedTrack() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFavourite, setIsFavourite] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration] = useState(240);
  const [randomColor, setRandomColor] = useState<string>("");

  useEffect(() => {
    const getRandomColor = (): string => {
      const colors = ["#949E7B", "#B3BF7D", "#758934", "#A1BA65", "#405A01"];
      const randomIndex = Math.floor(Math.random() * colors.length);
      return colors[randomIndex];
    };
    setRandomColor(getRandomColor());
  }, []);

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
      2,
      "0"
    )}`;
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleFavouriteToggle = () => {
    setIsFavourite(!isFavourite);
  };

  return (
    <div>
      <Container
        style={{
          height: "70vh",
          width: "30vw",
          margin: "auto",
          marginTop: "70px",
        }}
        arrow={true}
        link_arrow="/"
        direction="column"
      >
        <div
          className={styles.track__avatar}
          style={{ backgroundColor: randomColor }}
        ></div>

        <div className={styles.track__info}>
          <h2 className={styles.track__name}>Название трека</h2>
          <Link href="/author" className={styles.track__author}>
            <p className={styles.track__author}>Автор трека</p>
          </Link>

          <Link href="/track-info">
            <i className={`fa-solid fa-info ${styles.track__infoIcon}`}></i>
          </Link>
        </div>

        <div className={styles.track__progress}>
          <span className={styles.track__currentTime}>
            {formatTime(currentTime)}
          </span>
          <input
            type="range"
            min="0"
            max={duration}
            value={currentTime}
            onChange={(e) => setCurrentTime(Number(e.target.value))}
            className={styles.track__range}
          />
          <span className={styles.track__duration}>{formatTime(duration)}</span>
        </div>

        <div className={styles.track__controls}>
          <i className={`fa-solid fa-repeat ${styles.track__controlIcon}`}></i>
          <i
            className={`fa-solid fa-backward ${styles.track__controlIcon}`}
          ></i>

          <div className={styles.track__playPause} onClick={handlePlayPause}>
            {isPlaying ? (
              <i
                className={`fa-regular fa-circle-pause ${styles.track__controlIcon}`}
              ></i>
            ) : (
              <i
                className={`fa-regular fa-circle-play ${styles.track__controlIcon}`}
              ></i>
            )}
          </div>

          <i className={`fa-solid fa-forward ${styles.track__controlIcon}`}></i>

          <div onClick={handleFavouriteToggle}>
            {isFavourite ? (
              <i
                className={`fa-solid fa-star ${styles.track__controlIcon}`}
              ></i>
            ) : (
              <i
                className={`fa-regular fa-star ${styles.track__controlIcon}`}
              ></i>
            )}
          </div>
        </div>

        <div className={styles.track__controls}>
          <Link href="/select-playlist">
            <i className={`fa-solid fa-share ${styles.track__controlIcon}`}></i>
          </Link>
          <i className={`fa-solid fa-list-ul ${styles.track__controlIcon}`}></i>
        </div>
      </Container>
    </div>
  );
}
