"use client";

import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import { Playlist } from "@/entities/playlist";
import { Button } from "@/shared/button";
import styles from "./playlists.module.css";

export default function Playlists() {
  const router = useRouter();

  const Playlists = [
    { name: "Ммтао1", link: "/здфндшые1" },
    { name: "Ммтао2", link: "/здфндшые2" },
    { name: "Ммтао3", link: "/здфндшые3" },
    { name: "Ммтао4", link: "/здфндшые4" },
    { name: "Ммтао5", link: "/здфндшые5" },
  ];

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
        <div className={styles.playlists}>
          {Playlists.map((playlist, index) => (
            <Playlist
              key={index}
              name={playlist.name}
              link={playlist.link}
              showDelete={true}
            />
          ))}
        </div>
      </Container>

      <div className={styles.playlists_button}>
        <Button
          type="normal"
          color="green"
          disabled={false}
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
