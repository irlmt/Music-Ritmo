"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import styles from "./media.module.css";

export default function Media() {
  const router = useRouter();
  const [filePath, setFilePath] = useState<string | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const [isFileValid, setIsFileValid] = useState<boolean>(true);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;

    if (file) {
      const fileSizeLimit = 100 * 1024 * 1024;
      const fileSize = file.size;

      if (fileSize > fileSizeLimit) {
        setFileError(
          "Ошибка: слишком большой файл. Максимальный размер 100MBы"
        );
        setIsFileValid(false);
      } else {
        setFileError(null);
        setIsFileValid(true);
        setFilePath(file.name);
      }
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
        <h1 className={styles.create_playlists__title}>Медиатека</h1>

        <input type="file" id="file-input" hidden onChange={handleFileChange} />
        <label htmlFor="file-input" className={styles.media_input}>
          Укажите папку
        </label>

        {filePath && (
          <div className={styles.file_path}>
            <strong>Путь к файлу:</strong> {filePath}
          </div>
        )}

        {fileError && (
          <div className={styles.file_error}>
            <span>{fileError}</span>
          </div>
        )}

        <div style={{ display: "flex", justifyContent: "center" }}>
          <Button
            type="normal"
            color="green"
            disabled={!isFileValid}
            onClick={() => {
              router.push("/");
            }}
          >
            сканировать
          </Button>
        </div>
      </Container>
    </>
  );
}
