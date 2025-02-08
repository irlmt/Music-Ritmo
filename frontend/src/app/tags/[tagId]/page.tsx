"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import styles from "./tags.module.css";

interface Tag {
  id: number;
  tag: string;
  value: string;
}

export default function Tags() {
  const { tagId } = useParams();
  const decodedTagId =
    typeof tagId === "string" ? decodeURIComponent(tagId) : "";

  const [tags, setTags] = useState<Tag[]>([]);

  useEffect(() => {
    if (!decodedTagId) return;

    const fetchTags = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/specific/getTags?id=${decodedTagId}`
        );
        const data = await response.json();
        console.log("Полученные данные:", data); // Выводим в консоль

        // Проверяем, есть ли теги в ответе
        if (data["subsonic-response"]?.tags) {
          setTags(
            data["subsonic-response"].tags.map((tag: any) => ({
              id: tag.id,
              tag: tag.name,
              value: tag.value.toString(),
            }))
          );
        } else {
          console.error("Теги не найдены в ответе сервера");
        }
      } catch (error) {
        console.error("Ошибка при загрузке тегов:", error);
      }
    };

    fetchTags();
  }, [decodedTagId]);

  return (
    <>
      <Container
        style={{
          height: "65vh",
          width: "60vw",
          margin: "auto",
          marginTop: "50px",
        }}
        direction="column"
        arrow={true}
        link_arrow="/track"
      >
        <h1>Теги</h1>
        {decodedTagId && <p>Выбранный тег ID: {decodedTagId}</p>}
      </Container>
    </>
  );
}
