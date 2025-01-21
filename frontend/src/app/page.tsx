"use client";

import { useRouter } from "next/navigation";

import { Header } from "@/widgets/header";
import { SearchPanel } from "@/features/search-panel";
import { Playlist } from "@/entities/playlist";
import { Button } from "@/shared/button";
import styles from "./page.module.css";

export default function Home() {
  const router = useRouter();

  const Playlists = [
    { name: "Ммтао1", link: "/здфндшые1", showDelete: false },
    { name: "Ммтао2", link: "/здфндшые2", showDelete: false },
    { name: "Ммтао3", link: "/здфндшые3", showDelete: false },
    { name: "Ммтао4", link: "/здфндшые4", showDelete: false },
    { name: "Ммтао5", link: "/здфндшые5", showDelete: false },
  ];

  return (
    <>
      <Header />
      <SearchPanel />
      <div className={styles.home_playlists}>
        {Playlists.map((playlist, index) => (
          <Playlist
            key={index}
            name={playlist.name}
            link={playlist.link}
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
