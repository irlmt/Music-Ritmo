"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import styles from "./tags.module.css";

interface Tag {
  tag: string;
  value: string;
}

interface ServerResponse {
  album: string;
  album_artist: string;
  album_position: number;
  artists: string;
  genres: string;
  title: string;
  year: string;
}

export default function Tags() {
  const { tagId } = useParams();
  const decodedTagId =
    typeof tagId === "string" ? decodeURIComponent(tagId) : "";

  const [tags, setTags] = useState<Tag[]>([]);
  const [, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!decodedTagId) return;

    const fetchTags = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/specific/getTags?id=${decodedTagId}`
        );
        const data: ServerResponse = await response.json();

        console.log("Полученные данные:", data);

        setTags([
          { tag: "Album", value: data.album || "" },
          { tag: "Album Artist", value: data.album_artist || "" },
          { tag: "Title", value: data.title || "" },
          { tag: "Artists", value: data.artists || "" },
          { tag: "Genres", value: data.genres || "" },
          { tag: "Year", value: data.year || "" },
          {
            tag: "Album Position",
            value: data.album_position?.toString() || "",
          },
        ]);
        setError(null);
      } catch (error) {
        console.error("Ошибка при загрузке тегов:", error);
        setError("Ошибка при загрузке тегов.");
      }
    };

    fetchTags();
  }, [decodedTagId]);

  const handleTagChange = (
    tag: Tag,
    field: "tag" | "value",
    newValue: string
  ) => {
    setTags((prevTags) =>
      prevTags.map((t) => (t.tag === tag.tag ? { ...t, [field]: newValue } : t))
    );
  };

  const handleDeleteTag = (tag: Tag) => {
    if (tags.indexOf(tag) < 7) return;
    setTags((prevTags) => prevTags.filter((t) => t.tag !== tag.tag));
  };

  const handleClearTags = () => {
    setTags((prevTags) => prevTags.slice(0, 7));
  };

  const handleAddTag = () => {
    const newTagNumber = tags.length + 1;
    const newTag = {
      tag: `Новый тег ${newTagNumber}`,
      value: "0",
    };
    setTags([...tags, newTag]);
  };

  const handleSaveTags = async () => {
    try {
      const requestData = {
        album: tags.find((tag) => tag.tag === "Album")?.value || "",
        album_artist:
          tags.find((tag) => tag.tag === "Album Artist")?.value || "",
        album_position:
          tags.find((tag) => tag.tag === "Album Position")?.value?.toString() ||
          "",
        artists: tags.find((tag) => tag.tag === "Artists")?.value || "",
        genres: tags.find((tag) => tag.tag === "Genres")?.value || "",
        title: tags.find((tag) => tag.tag === "Title")?.value || "",
        year: tags.find((tag) => tag.tag === "Year")?.value || "",
      };

      const response = await fetch(
        `http://localhost:8000/specific/updateTags?id=${decodedTagId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        }
      );

      if (response.ok) {
        console.log("Теги успешно сохранены!");
      } else {
        console.log("Ошибка при сохранении тегов.");
      }
    } catch (error) {
      console.error("Ошибка при сохранении тегов:", error);
      console.log("Ошибка при сохранении тегов.");
    }
  };

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
        link_arrow={`/track/${decodedTagId}`}
      >
        <div className={styles.tags}>
          <h1>Теги</h1>

          <table className={styles.tags_table}>
            <tbody>
              {tags.map((tag) => (
                <tr key={tag.tag} className={styles.tagRow}>
                  <td>
                    <input
                      type="text"
                      value={tag.tag}
                      onChange={(e) =>
                        handleTagChange(tag, "tag", e.target.value)
                      }
                      className={styles.inputTag}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      value={tag.value}
                      onChange={(e) =>
                        handleTagChange(tag, "value", e.target.value)
                      }
                      className={styles.inputValue}
                    />
                  </td>
                  {tags.indexOf(tag) >= 7 && (
                    <td
                      className={styles.deleteIconWrapper}
                      onClick={() => handleDeleteTag(tag)}
                    >
                      <i
                        className={`fa-solid fa-xmark ${styles.deleteIcon}`}
                      ></i>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className={styles.tags_button}>
          <Button
            type="normal"
            color="green"
            disabled={false}
            onClick={handleAddTag}
          >
            добавить тег
          </Button>
          <Button
            type="normal"
            color="white"
            disabled={false}
            onClick={handleClearTags}
          >
            очистить все
          </Button>
          <Button
            type="normal"
            color="green"
            disabled={false}
            onClick={handleSaveTags}
          >
            сохранить
          </Button>
        </div>
      </Container>
    </>
  );
}
