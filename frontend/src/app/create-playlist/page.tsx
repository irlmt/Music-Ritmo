"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import { Input } from "@/shared/input";
import { Button } from "@/shared/button";
import styles from "./create_playlist.module.css";

export default function CreatePlaylist() {
  const router = useRouter();
  const [playlistName, setPlaylistName] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreatePlaylist = async () => {
    if (!playlistName) {
      setError("Название плейлиста не может быть пустым");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const userLogin = "test_user";

      const response = await fetch(
        `http://localhost:8000/rest/createPlaylist?name=${encodeURIComponent(
          playlistName
        )}&u=${encodeURIComponent(userLogin)}`,
        {
          method: "GET",
        }
      );

      const data = await response.json();

      if (data["subsonic-response"].status === "ok") {
        router.push("/playlists");
      } else {
        setError("Не удалось создать плейлист");
      }
    } catch {
      setError("Произошла ошибка при создании плейлиста");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Container
        style={{
          height: "35vh",
          width: "50vw",
          margin: "auto",
          marginTop: "50px",
        }}
        direction="column"
        arrow={true}
        link_arrow="/playlists"
      >
        <h1 className={styles.create_playlists__title}>Создание плейлиста</h1>
        <Input
          placeholder="Название плейлиста"
          value={playlistName}
          onChange={(e) => setPlaylistName(e.target.value)}
        />
        {error && <div className={styles.error}>{error}</div>}{" "}
        <Button
          type="normal"
          color="green"
          disabled={loading}
          onClick={handleCreatePlaylist}
        >
          {loading ? "Создание..." : "Создать плейлист"}
        </Button>
      </Container>
    </>
  );
}
