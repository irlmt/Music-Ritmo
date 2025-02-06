"use client";

import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import { useState } from "react";
import styles from "./media.module.css";

export default function Media() {
  const [scanStatus, setScanStatus] = useState("");

  const startScan = async () => {
    try {
      const response = await fetch("http://localhost:8000/rest/startScan", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (response.ok && data["subsonic-response"].status === "ok") {
        setScanStatus("Сканирование выполнено успешно!");
        setTimeout(() => setScanStatus(""), 1500);
      } else {
        setScanStatus("Ошибка при запуске сканирования");
      }
    } catch (error) {
      console.error("Error during scan initiation:", error);
      setScanStatus("Ошибка при запуске сканирования");
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
        link_arrow="/"
      >
        <h1>Медиатека</h1>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <Button type="normal" color="green" onClick={startScan}>
            Запустить сканирование
          </Button>
        </div>

        {scanStatus && <div className={styles.message}>{scanStatus}</div>}
      </Container>
    </>
  );
}
