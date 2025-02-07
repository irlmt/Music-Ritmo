"use client";

import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import { useState, useEffect } from "react";
import { Tracklist } from "@/widgets/track-list";
import styles from "./playlist.module.css";
import { useParams } from "next/navigation";

interface Track {
  id: string;
  title: string;
  artist: string;
  artistId: string;
  favourite?: boolean;
  duration: number;
}

interface Playlist {
  id: string;
  name: string;
  entry: Track[];
}

export default function Playlist() {
  const router = useRouter();
  const { playlistId } = useParams();
  const [playlistData, setPlaylistData] = useState<Playlist | null>(null);

  useEffect(() => {
    if (!playlistId) return;

    const fetchPlaylistData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/rest/getPlaylist?id=${playlistId}`
        );
        const data = await response.json();

        console.log("Ответ от бека:", data);

        if (
          data["subsonic-response"] &&
          data["subsonic-response"].status === "ok"
        ) {
          const playlist: Playlist = {
            id: data["subsonic-response"].playlist.id,
            name: data["subsonic-response"].playlist.name,
            entry: data["subsonic-response"].playlist.entry.map(
              (track: Track) => ({
                id: track.id,
                title: track.title,
                artist: track.artist,
                artistId: track.artistId,
                favourite: track.favourite || false,
                duration: track.duration,
              })
            ),
          };
          setPlaylistData(playlist);
        } else {
          console.error("Ошибка при получении данных о плейлисте", data);
        }
      } catch (error) {
        console.error("Ошибка при запросе:", error);
      }
    };

    fetchPlaylistData();
  }, [playlistId]);

  const handleRemove = (index: number) => {
    setPlaylistData((prev: Playlist | null) => {
      if (prev) {
        const updatedEntries = prev.entry.filter((_, i) => i !== index);
        return { ...prev, entry: updatedEntries };
      }
      return prev;
    });
  };

  const handleFavouriteToggle = (index: number) => {
    setPlaylistData((prev: Playlist | null) => {
      if (prev) {
        const updatedEntries = [...prev.entry];
        updatedEntries[index] = {
          ...updatedEntries[index],
          favourite: !updatedEntries[index].favourite,
        };
        return { ...prev, entry: updatedEntries };
      }
      return prev;
    });
  };

  if (!playlistData) {
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
        <h1 className={styles.playlist__title}>{playlistData.name}</h1>
        <div className={styles.playlist}>
          {playlistData.entry.map((track, index) => (
            <Tracklist
              key={index}
              name={track.title}
              name_link={`/track/${track.id}`}
              artist={track.artist}
              artist_link={`/artist/${track.artistId}`}
              favourite={true}
              time={track.duration}
              onRemove={() => handleRemove(index)}
              showRemoveButton={true}
              onFavouriteToggle={() => handleFavouriteToggle(index)}
            />
          ))}
        </div>
      </Container>

      <div className={styles.playlist_button}>
        <Button
          type="normal"
          color="green"
          disabled={false}
          onClick={() => {
            router.push("/rename-playlist");
          }}
        >
          редактировать
        </Button>
      </div>
    </>
  );
}
