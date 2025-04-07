"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Container } from "@/shared/container";
import { Tracklist } from "@/widgets/track-list";
import { useAuth } from "@/app/auth-context";
import styles from "./album.module.css";

interface Track {
  id: string;
  title: string;
  artist: string;
  artistId: string;
  duration: number;
  path: string;
  starred: string;
}

interface Album {
  id: string;
  name: string;
  tracks: Track[];
}

export default function Album() {
  const { albumId } = useParams();
  const [album, setAlbum] = useState<Album | null>(null);
  const [, setStarredTracks] = useState<Track[]>([]);
  const { user, password } = useAuth();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!albumId || !user || !password) {
      setLoading(false);
      return;
    }

    const fetchAlbumData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/rest/getAlbum?id=${albumId}&username=${user}&u=${user}&p=${password}`
        );

        if (!response.ok) {
          console.error(
            "Ошибка при получении данных с сервера:",
            response.status
          );
          return;
        }

        const data = await response.json();
        const albumData = data["subsonic-response"]?.album;

        if (albumData) {
          const tracks = Array.isArray(albumData.song)
            ? albumData.song.map((track: Track) => ({
                ...track,
                starred: track.starred || "",
              }))
            : [];

          setAlbum({
            id: albumData.id || "",
            name: albumData.name || "",
            tracks,
          });
        } else {
          console.error("Данные об альбоме не найдены");
        }
      } catch (error) {
        console.error("Ошибка при загрузке данных альбома:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlbumData();
  }, [albumId, user, password]);

  const handleFavouriteToggle = async (
    trackId: string,
    currentStatus: string
  ) => {
    if (!user || !password) return;

    const action = currentStatus ? "unstar" : "star";
    const url = `http://localhost:8000/rest/${action}?id=${trackId}&username=${user}&u=${user}&p=${password}`;

    try {
      const response = await fetch(url);
      const data = await response.json();

      if (data["subsonic-response"].status === "ok") {
        setStarredTracks((prevTracks) =>
          prevTracks.filter((track) => track.id !== trackId)
        );
        window.location.reload();
      }
    } catch (error) {
      console.error("Ошибка при изменении статуса избранного:", error);
    }
  };

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (!album) {
    return <div>Ошибка загрузки альбома</div>;
  }

  return (
    <Container
      style={{
        height: "65vh",
        width: "85vw",
        margin: "auto",
        marginTop: "50px",
      }}
      direction="column"
      arrow={true}
    >
      <h1 className={styles.playlist__title}>{album.name}</h1>
      <div className={styles.playlist}>
        {album.tracks.length > 0 ? (
          album.tracks.map((track) => (
            <Tracklist
              key={track.id}
              name={track.title}
              name_link={`/track/${track.id}`}
              artist={track.artist}
              artist_link={`/artist/${track.artistId}`}
              favourite={track.starred}
              time={track.duration}
              showRemoveButton={false}
              onFavouriteToggle={() =>
                handleFavouriteToggle(track.id, track.starred)
              }
            />
          ))
        ) : (
          <p>Треки не найдены.</p>
        )}
      </div>
    </Container>
  );
}
