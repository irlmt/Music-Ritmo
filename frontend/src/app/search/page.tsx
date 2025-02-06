"use client";

import { Container } from "@/shared/container";
import { useState, useEffect } from "react";
import { Tracklist } from "@/widgets/track-list";
import { Playlist } from "@/entities/playlist";
import { Artist } from "@/entities/artist";
import styles from "./search.module.css";
import { useSearchParams } from "next/navigation";

interface Song {
  id: string;
  title: string;
  artist: string;
  album: string;
  genre: string;
  additionalData?: Record<string, unknown>;
}

interface Album {
  id: string;
  title: string;
  artist: string;
}

interface Artist {
  id: string;
  artist: string;
}

interface SearchResult {
  id: string;
  title: string;
  artist: string;
  album: string;
  name: string;
  type: "song" | "album" | "artist";
}

export default function SearchResultsPage() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [query, setQuery] = useState<string>("");

  const searchParams = useSearchParams();
  const queryParam = searchParams.get("query");

  useEffect(() => {
    if (queryParam) {
      setQuery(queryParam);

      const fetchResults = async () => {
        if (queryParam && queryParam.length > 0) {
          try {
            const response = await fetch(
              `http://localhost:8000/rest/search3?query=${queryParam}&songCount=100&albumCount=100&artistCount=100&songOffset=0&albumOffset=0&artistOffset=0`
            );
            const data = await response.json();

            if (
              data["subsonic-response"] &&
              data["subsonic-response"].status === "ok"
            ) {
              const searchResult = [
                ...data["subsonic-response"].searchResult3.song.map(
                  (song: Song) => ({
                    ...song,
                    type: "song",
                  })
                ),
                ...data["subsonic-response"].searchResult3.album.map(
                  (album: Album) => ({
                    ...album,
                    type: "album",
                  })
                ),
                ...data["subsonic-response"].searchResult3.artist.map(
                  (artist: Artist) => ({
                    ...artist,
                    type: "artist",
                  })
                ),
              ];
              setResults(searchResult);
            } else {
              setResults([]);
            }
          } catch (error) {
            console.error("Ошибка при запросе:", error);
            setResults([]);
          }
        }
      };

      fetchResults();
    }
  }, [queryParam]);

  const albums = results.filter((result) => result.type === "album");
  const artist = results.filter((result) => result.type === "artist");
  const songs = results.filter((result) => result.type === "song");

  return (
    <>
      <Container
        style={{
          height: "75vh",
          width: "85vw",
          margin: "auto",
          marginTop: "50px",
        }}
        direction="column"
        arrow={true}
        link_arrow="/"
      >
        <h1 className={styles.playlist__title}>
          Результаты поиска для {query}
        </h1>

        <div className={styles.playlist}>
          <div className={styles.album_playlists}>
            {albums.length > 0 && (
              <div className={styles.album_playlists}>
                {albums.map((album, index) => (
                  <Playlist
                    key={index}
                    name={album.title}
                    link={`/album/${album.id}`}
                    showDelete={false}
                  />
                ))}
              </div>
            )}
          </div>

          <div className={styles.album_playlists}>
            {artist.length > 0 && (
              <div className={styles.album_playlists}>
                {artist.map((artist, index) => (
                  <Artist
                    key={index}
                    name={artist.name}
                    link={`/artist/${artist.id}`}
                  />
                ))}
              </div>
            )}
          </div>

          <div className={styles.tracklist}>
            {songs.length > 0 && (
              <div>
                {songs.map((song, index) => (
                  <Tracklist
                    key={index}
                    name={song.title}
                    name_link={`/track/${song.id}`}
                    artist={song.artist}
                    artist_link={`/artist/${song.artist}`}
                    favourite={false}
                    time={0}
                    showRemoveButton={false}
                    onFavouriteToggle={() => {}}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </Container>
    </>
  );
}
