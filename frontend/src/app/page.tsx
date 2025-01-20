"use client";

import { useRouter } from "next/navigation";

import { Header } from "@/widgets/header";
import { SearchPanel } from "@/features/search-panel";
import { Playlist } from "@/entities/playlist";
import { Button } from "@/shared/button";
import styles from "./page.module.css";

export default function Home() {
  const router = useRouter();

  return (
    <>
      <Header />
      <SearchPanel />
      <div className={styles.home_playlists}>
        <Playlist name="Ммтао1" link="/здфндшые1" />
        <Playlist name="Ммтао2" link="/здфндшые2" />
        <Playlist name="Ммтао3" link="/здфндшые3" />
        <Playlist name="Ммтао4" link="/здфндшые4" />
        <Playlist name="Ммтао5" link="/здфндшые5" />
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
