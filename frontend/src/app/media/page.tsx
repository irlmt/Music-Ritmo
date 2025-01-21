"use client";

import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import styles from "./media.module.css";

export default function Media() {
  const router = useRouter();

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
        link_arrow="/"
      >
        <h1 className={styles.create_playlists__title}>Медиатека</h1>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <Button
            type="normal"
            color="green"
            onClick={() => {
              router.push("/");
            }}
          >
            запустить сканирование
          </Button>
        </div>
      </Container>
    </>
  );
}
