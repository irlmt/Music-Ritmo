"use client";

import { Container } from "@/shared/container";
import { Playlist } from "@/entities/playlist";
import styles from "./select-playlist.module.css";

export default function Playlists() {
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
        link_arrow="/track"
      >
        <h1 className={styles.playlists__title}>Выберите плейлист</h1>
        <div className={styles.playlists}>
          <Playlist name="Ммтао1" link="/здфндшые1" showDelete={false} />
          <Playlist name="Ммтао2" link="/здфндшые2" showDelete={false} />
          <Playlist name="Ммтао3" link="/здфндшые3" showDelete={false} />
          <Playlist name="Ммтао4" link="/здфндшые4" showDelete={false} />
          <Playlist name="Ммтао5" link="/здфндшые5" showDelete={false} />
          <Playlist name="Ммтао1" link="/здфндшые1" showDelete={false} />
        </div>
      </Container>
    </>
  );
}
