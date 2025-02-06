"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Container } from "@/shared/container";
import { Tracklist } from "@/widgets/track-list";
import styles from "./genre.module.css";

interface Track {
  id: string;
  title: string;
  artist: string;
  duration: number;
  path: string;
  favourite: boolean;
}

export default function TracksGenre() {
  const { genreName } = useParams();
  const [tracks, setTracks] = useState<Track[]>([]);

  const decodedGenreName =
    typeof genreName === "string" ? decodeURIComponent(genreName) : "";

  useEffect(() => {
    if (!genreName) return;

    const fetchTracks = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/rest/getSongsByGenre?genre=${genreName}`
        );
        const data = await response.json();
        const songs = data["subsonic-response"]?.songsByGenre?.song;

        if (songs && songs.length > 0) {
          const tracksData = songs.map(
            (track: {
              id: string;
              title: string;
              artist: string;
              duration: number;
              path: string;
            }) => ({
              id: track.id,
              title: track.title,
              artist: track.artist,
              duration: Math.floor(track.duration),
              path: track.path,
              favourite: false,
            })
          );

          setTracks(tracksData);
        } else {
          console.error("Треки не найдены в ответе сервера");
        }
      } catch (error) {
        console.error("Ошибка при загрузке треков:", error);
      }
    };

    fetchTracks();
  }, [genreName]);

  const handleFavouriteToggle = (index: number) => {
    setTracks((prevTracks) =>
      prevTracks.map((track, i) =>
        i === index ? { ...track, favourite: !track.favourite } : track
      )
    );
  };

  return (
    <>
      <Container
        style={{
          height: "65vh",
          width: "85vw",
          margin: "auto",
          marginTop: "50px",
        }}
        direction="column"
        arrow={true}
        link_arrow="/"
      >
        <h1 className={styles.playlist__title}>{decodedGenreName}</h1>
        <div className={styles.playlist}>
          {tracks.length > 0 ? (
            tracks.map((track, index) => (
              <Tracklist
                key={track.id}
                name={track.title}
                name_link={`/track/${track.id}`}
                author={track.artist}
                author_link={`/author/${track.artist}`}
                favourite={track.favourite}
                time={track.duration}
                showRemoveButton={false}
                onFavouriteToggle={() => handleFavouriteToggle(index)}
              />
            ))
          ) : (
            <p>Треки не найдены.</p>
          )}
        </div>
      </Container>
    </>
  );
}
