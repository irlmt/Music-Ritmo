"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/widgets/header";
import { SearchPanel } from "@/features/search-panel";
import { Button } from "@/shared/button";
import { Playlist } from "@/entities/playlist";
import styles from "./page.module.css";

interface Genre {
  value: string;
}

export default function Home() {
  const router = useRouter();
  const [genres, setGenres] = useState<Genre[]>([]);

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        const response = await fetch("http://localhost:8000/rest/getGenres");
        const data = await response.json();

        const genresData = data["subsonic-response"].genres.genre;

        if (genresData) {
          setGenres(genresData);
        }
      } catch (error) {
        console.error("Ошибка при загрузке жанров:", error);
      }
    };

    fetchGenres();
  }, []);

  return (
    <>
      <Header />
      <SearchPanel />
      <div className={styles.home_playlists}>
        {genres.map((genre, index) => (
          <Playlist
            key={index}
            name={genre.value}
            link={`/genre/${genre.value}`}
            showDelete={false}
          />
        ))}
      </div>

      <div className={styles.home_button}>
        <Button
          type="normal"
          color="green"
          disabled={false}
          onClick={() => {
            router.push("/media");
          }}
        >
          медиатека
        </Button>
      </div>
    </>
  );
}
