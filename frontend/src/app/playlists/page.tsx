"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import { Playlist } from "@/entities/playlist";
import { Button } from "@/shared/button";
import { useAuth } from "@/app/auth-context";
import styles from "./playlists.module.css";

type PlaylistType = {
  id: string;
  name: string;
  owner: string;
  public: boolean;
  created: string;
  changed: string;
  songCount: number;
  duration: number;
};

export default function Playlists() {
  const router = useRouter();
  const { user, password } = useAuth();
  const [playlists, setPlaylists] = useState<PlaylistType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user || !password) {
      setError("Ошибка авторизации. Войдите в систему.");
      setLoading(false);
      return;
    }

    const fetchPlaylists = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/rest/getPlaylists?username=${user}&u=${user}&p=${password}`
        );
        const data = await response.json();

        if (data["subsonic-response"].status === "ok") {
          const fetchedPlaylists = data["subsonic-response"].playlists.playlist;

          if (fetchedPlaylists.length === 0) {
            setError("У вас нет плейлистов");
          } else {
            setPlaylists(fetchedPlaylists);
            setError(null);
          }
        } else {
          setError("Не удалось загрузить плейлисты");
        }
      } catch {
        setError("Произошла ошибка при получении плейлистов");
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, [user, password]);

  const handleDelete = (id: string) => {
    setPlaylists(playlists.filter((playlist) => playlist.id !== id));
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
        <h1 className={styles.playlists__title}>Ваши плейлисты</h1>
        {error && <div className={styles.message}>{error}</div>}

        <div className={styles.playlists}>
          {!loading &&
            !error &&
            playlists.length > 0 &&
            playlists.map((playlist) => (
              <Playlist
                key={playlist.id}
                name={playlist.name}
                link={`/playlist/${playlist.id}`}
                showDelete={true}
                playlist_id={playlist.id}
                onDelete={handleDelete}
              />
            ))}
        </div>
      </Container>

      {playlists.length >= 30 && (
        <div className={styles.message_more}>Слишком много плейлистов</div>
      )}
      <div className={styles.playlists_button}>
        <Button
          type="normal"
          color="green"
          disabled={playlists.length >= 30}
          onClick={() => {
            router.push("/create-playlist");
          }}
        >
          создать плейлист
        </Button>
      </div>
    </>
  );
}
