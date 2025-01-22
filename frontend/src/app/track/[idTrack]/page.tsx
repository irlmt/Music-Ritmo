"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./track.module.css";

interface TrackData {
  title: string;
  artist: string;
  genre: string;
}

export default function PlayedTrack() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFavourite, setIsFavourite] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [randomColor, setRandomColor] = useState<string>("");
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [trackId, setTrackId] = useState<number>(1);
  const [trackData, setTrackData] = useState<TrackData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    const idFromUrl = pathname?.split("/")[2];
    if (idFromUrl) {
      setTrackId(parseInt(idFromUrl));
    }
  }, [pathname]);

  useEffect(() => {
    const getRandomColor = (): string => {
      const colors = ["#949E7B", "#B3BF7D", "#758934", "#A1BA65", "#405A01"];
      const randomIndex = Math.floor(Math.random() * colors.length);
      return colors[randomIndex];
    };
    setRandomColor(getRandomColor());

    const fetchTrack = async (id: number) => {
      try {
        const response = await fetch(
          `http://localhost:8000/rest/stream?id=${id}`
        );
        if (!response.ok) {
          throw new Error("Ошибка при получении трека");
        }
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioUrl(audioUrl);
      } catch (error) {
        console.error("Ошибка при загрузке трека:", error);
      }
    };

    const fetchTrackData = async (id: number) => {
      setIsLoading(true);
      try {
        const response = await fetch(
          `http://localhost:8000/rest/getSong?id=${id}`
        );
        if (!response.ok) {
          throw new Error("Ошибка при получении данных о треке");
        }
        const data = await response.json();
        console.log("Полученные данные о треке:", data);

        if (data?.["subsonic-response"]?.song) {
          const track = data["subsonic-response"].song;
          setTrackData({
            title: track.title || "Неизвестное название",
            artist: track.artist || "Неизвестный автор",
            genre: track.genre || "Неизвестный жанр",
          });
        } else {
          console.error("Данные о треке не найдены:", data);
          setTrackData({
            title: "Неизвестное название",
            artist: "Неизвестный автор",
            genre: "Неизвестный жанр",
          });
        }
      } catch (error) {
        console.error("Ошибка при загрузке данных о треке:", error);
        setTrackData({
          title: "Неизвестное название",
          artist: "Неизвестный автор",
          genre: "Неизвестный жанр",
        });
      } finally {
        setIsLoading(false);
      }
    };

    if (trackId) {
      fetchTrack(trackId);
      fetchTrackData(trackId);
    }
  }, [trackId]);

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
      2,
      "0"
    )}`;
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
      setDuration(audioRef.current.duration);
    }
  };

  const handleFavouriteToggle = () => {
    setIsFavourite(!isFavourite);
  };

  const handleForward = () => {
    const nextTrackId = trackId + 1;
    setTrackId(nextTrackId);
    router.push(`/track/${nextTrackId}`);
  };

  const handleBackward = () => {
    router.back();
  };

  if (isLoading) {
    return <div>Загрузка...</div>;
  }

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
        link_arrow={`/genre/${trackData?.genre}`}
        direction="column"
      >
        <div
          className={styles.track__avatar}
          style={{ backgroundColor: randomColor }}
        ></div>

        <div className={styles.track__info}>
          <h2 className={styles.track__name}>
            {trackData ? trackData.title : "Загрузка названия трека..."}
          </h2>
          <Link
            href={`/author/${trackData?.artist}`}
            className={styles.track__author}
          >
            <p className={styles.track__author}>
              {trackData ? trackData.artist : "Загрузка автора..."}
            </p>
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
            max={duration || 0}
            value={currentTime}
            onChange={(e) => {
              if (audioRef.current) {
                audioRef.current.currentTime = Number(e.target.value);
                setCurrentTime(Number(e.target.value));
              }
            }}
            className={styles.track__range}
          />
          <span className={styles.track__duration}>{formatTime(duration)}</span>
        </div>

        <div className={styles.track__controls}>
          <i className={`fa-solid fa-repeat ${styles.track__controlIcon}`}></i>

          <i
            className={`fa-solid fa-backward ${styles.track__controlIcon}`}
            onClick={handleBackward}
          />

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

          <i
            className={`fa-solid fa-forward ${styles.track__controlIcon}`}
            onClick={handleForward}
          />

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

      {audioUrl && (
        <audio
          ref={audioRef}
          src={audioUrl}
          onTimeUpdate={handleTimeUpdate}
          onEnded={() => setIsPlaying(false)}
        />
      )}
    </div>
  );
}
