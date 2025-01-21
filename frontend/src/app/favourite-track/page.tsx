"use client";

import { Container } from "@/shared/container";
import { useState } from "react";
import { Tracklist } from "@/widgets/track-list";
import styles from "./favourite-track.module.css";

export default function FavouriteTrack() {
  const [playlists, setPlaylists] = useState([
    {
      name: "Chill Vibes",
      name_link: "/track1",
      author: "DJ Relax",
      author_link: "/author1",
      favourite: true,
      time: 216,
    },
    {
      name: "Top 40 Hits",
      name_link: "/track1",
      author: "Hitmaker",
      author_link: "/author1",
      favourite: true,
      time: 180,
    },
    {
      name: "Workout Mix",
      name_link: "/track1",
      author: "Fitness Beats",
      author_link: "/author1",
      favourite: true,
      time: 240,
    },
  ]);

  const toggleFavourite = (index: number) => {
    const updatedPlaylists = [...playlists];
    updatedPlaylists[index].favourite = false;
    setPlaylists(updatedPlaylists.filter((playlist) => playlist.favourite));
  };

  const favouritePlaylists = playlists.filter((playlist) => playlist.favourite);

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
        <h1 className={styles.playlist__title}>Избранные треки</h1>
        <div className={styles.playlist}>
          {favouritePlaylists.map((playlist, index) => (
            <Tracklist
              key={index}
              name={playlist.name}
              name_link={playlist.name_link}
              author={playlist.author}
              author_link={playlist.author_link}
              favourite={playlist.favourite}
              time={playlist.time}
              showRemoveButton={false}
              onFavouriteToggle={() => toggleFavourite(index)}
            />
          ))}
        </div>
      </Container>
    </>
  );
}
