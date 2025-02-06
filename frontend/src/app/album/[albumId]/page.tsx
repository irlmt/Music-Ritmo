"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Container } from "@/shared/container";
import { Tracklist } from "@/widgets/track-list";
import styles from "./album.module.css";

interface Track {
  id: string;
  title: string;
  artist: string;
  artistId: string;
  duration: number;
  path: string;
  favourite: boolean;
}

interface Album {
  id: string;
  name: string;
  tracks: Track[];
}

export default function Album() {
  const { albumId } = useParams();
  const [album, setAlbum] = useState<Album | null>(null);

  useEffect(() => {
    if (albumId) {
      const fetchAlbumData = async () => {
        try {
          const response = await fetch(
            `http://localhost:8000/rest/getAlbum?id=${albumId}`
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
            const tracks = albumData.song.map(
              (track: {
                id: string;
                title: string;
                artist: string;
                artistId: string;
                duration: number;
                path: string;
              }) => ({
                id: track.id,
                title: track.title,
                artist: track.artist,
                artistId: track.artistId,
                duration: track.duration,
                path: track.path,
                favourite: false,
              })
            );

            setAlbum({
              id: albumData.id || "",
              name: albumData.name || "",
              tracks,
            });
          } else {
            console.error("Данные о альбоме не найдены");
          }
        } catch (error) {
          console.error("Ошибка при загрузке данных альбома:", error);
        }
      };

      fetchAlbumData();
    } else {
      console.error("Не передан ID альбома");
    }
  }, [albumId]);

  const handleFavouriteToggle = (index: number) => {
    if (album) {
      setAlbum((prevAlbum) => {
        if (!prevAlbum) return null;

        const updatedTracks = prevAlbum.tracks.map((track, i) =>
          i === index ? { ...track, favourite: !track.favourite } : track
        );
        return { ...prevAlbum, tracks: updatedTracks };
      });
    }
  };

  if (!album) {
    return <div>Загрузка...</div>;
  }

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
        <h1 className={styles.playlist__title}>{album.name}</h1>
        <div className={styles.playlist}>
          {album.tracks.length > 0 ? (
            album.tracks.map((track, index) => (
              <Tracklist
                key={track.id}
                name={track.title}
                name_link={`/track/${track.id}`}
                artist={track.artist}
                artist_link={`/artist/${track.artistId}`}
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
