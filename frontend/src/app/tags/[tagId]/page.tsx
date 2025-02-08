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
  const { id } = useParams();
  const [tags, setTags] = useState<Tag[]>([]);

  useEffect(() => {
    if (id) {
      const fetchTags = async () => {
        try {
          const response = await fetch(
            `http://localhost:8000/getTags?id=${id}`
          );
          if (!response.ok) {
            throw new Error("Ошибка при получении данных с сервера");
          }
          const data = await response.json();
          console.log("Ответ от сервера:", data);

          const tagsData: Tag[] = Object.entries(data).map(([key, value]) => ({
            tag: key,
            value: String(value),
            id: tags.length + 1,
          }));

          setTags(tagsData);
        } catch (error) {
          console.error("Ошибка при получении данных с сервера:", error);
        }
      };

      fetchTags();
    }
  }, [id]);

  const handleAddTag = () => {
    const newTag: Tag = {
      id: tags.length + 1,
      tag: "Новый тег",
      value: "0",
    };
    setTags([...tags, newTag]);
  };

  const handleTagChange = (
    id: number,
    field: "tag" | "value",
    value: string
  ) => {
    setTags(
      tags.map((tag) => (tag.id === id ? { ...tag, [field]: value } : tag))
    );
  };

  const handleClearTags = () => {
    setTags([]);
  };

  const handleDeleteTag = (id: number) => {
    setTags(tags.filter((tag) => tag.id !== id));
  };

  const handleSaveTags = async () => {
    const updatedTags = tags.reduce((acc, tag) => {
      acc[tag.tag] = tag.value;
      return acc;
    }, {} as Record<string, string>);

    try {
      const response = await fetch(
        `http://localhost:8000/updateTags?id=${id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updatedTags),
        }
      );

      if (!response.ok) {
        throw new Error("Ошибка при обновлении тегов");
      }

      console.log("Теги успешно обновлены");
    } catch (error) {
      console.error("Ошибка при сохранении тегов:", error);
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
        link_arrow="/track"
      >
        <h1>Теги</h1>
        <div className={styles.tags}>
          <table className={styles.tags_table}>
            <tbody>
              {tags.map((tag) => (
                <tr key={tag.id} className={styles.tagRow}>
                  <td>
                    <input
                      type="text"
                      value={tag.tag}
                      onChange={(e) =>
                        handleTagChange(tag.id, "tag", e.target.value)
                      }
                      className={styles.inputTag}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      value={tag.value}
                      onChange={(e) =>
                        handleTagChange(tag.id, "value", e.target.value)
                      }
                      className={styles.inputValue}
                    />
                  </td>
                  <td
                    className={styles.deleteIconWrapper}
                    onClick={() => handleDeleteTag(tag.id)}
                  >
                    <i className={`fa-solid fa-xmark ${styles.deleteIcon}`}></i>
                  </td>
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
