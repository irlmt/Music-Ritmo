"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/widgets/header";
import { SearchPanel } from "@/features/search-panel";
import { Button } from "@/shared/button";
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
        const response = await fetch("/api/genres");
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

  const handleGenreClick = (genreName: string) => {
    router.push(`/genre/${genreName}`);
  };

  return (
    <>
      <Header />
      <SearchPanel />
      <div className={styles.home_playlists}>
        {genres.map((genre, index) => (
          <div
            key={index}
            className={styles.genre_item}
            onClick={() => handleGenreClick(genre.value)}
          >
            <h3>{genre.value}</h3>
          </div>
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
