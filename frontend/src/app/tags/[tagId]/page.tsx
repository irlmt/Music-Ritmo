"use client";

import { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import { Container } from "@/shared/container";
import { Button } from "@/shared/button";
import styles from "./tags.module.css";

interface Tag {
  tag: string;
  value: string;
}

interface ServerResponse {
  [key: string]: string | number;
}

export default function Tags() {
  const { tagId } = useParams();
  const decodedTagId =
    typeof tagId === "string" ? decodeURIComponent(tagId) : "";

  const [tags, setTags] = useState<Tag[]>([]);
  const [hoveredRow, setHoveredRow] = useState<number | null>(null);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    if (!decodedTagId) return;

    const fetchTags = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/specific/getTags?id=${decodedTagId}`
        );
        const data: ServerResponse = await response.json();

        const newTags = Object.keys(data).map((key) => ({
          tag: key,
          value: data[key]?.toString() || "",
        }));

        setTags(newTags);
      } catch (error) {
        console.error("Ошибка при загрузке тегов:", error);
      }
    };

    fetchTags();
  }, [decodedTagId]);

  const handleTagChange = (
    tag: Tag,
    field: "tag" | "value",
    newValue: string,
    index: number
  ) => {
    setTags((prevTags) =>
      prevTags.map((t) => (t.tag === tag.tag ? { ...t, [field]: newValue } : t))
    );

    setTimeout(() => {
      if (field === "tag") {
        inputRefs.current[index]?.focus();
      } else {
        inputRefs.current[index + tags.length]?.focus();
      }
    }, 0);
  };

  const handleDeleteTag = (index: number) => {
    setTags((prevTags) => prevTags.filter((_, i) => i !== index));
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
      const requestData: ServerResponse = {};

      tags.forEach((tag) => {
        requestData[tag.tag] = tag.value;
      });

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
        const errorData = await response.json();
        console.log("Ошибка при сохранении тегов:", errorData);
      }
    } catch (error) {
      console.error("Ошибка при сохранении тегов:", error);
    }
  };

  return (
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
            {tags.map((tag, index) => (
              <tr
                key={tag.tag}
                className={styles.tagRow}
                onMouseEnter={() => index >= 7 && setHoveredRow(index)}
                onMouseLeave={() => setHoveredRow(null)}
              >
                <td>
                  <input
                    type="text"
                    value={tag.tag}
                    onChange={(e) =>
                      handleTagChange(tag, "tag", e.target.value, index)
                    }
                    className={styles.inputTag}
                    ref={(el) => {
                      inputRefs.current[index] = el;
                    }}
                  />
                </td>
                <td>
                  <input
                    type="text"
                    value={tag.value}
                    onChange={(e) =>
                      handleTagChange(tag, "value", e.target.value, index)
                    }
                    className={styles.inputValue}
                  />
                </td>
                {index >= 7 && hoveredRow === index && (
                  <td
                    className={styles.deleteIconWrapper}
                    onClick={() => handleDeleteTag(index)}
                  >
                    <i className={`fa-solid fa-xmark ${styles.deleteIcon}`}></i>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className={styles.tags_button}>
        <Button type="normal" color="green" onClick={handleAddTag}>
          добавить тег
        </Button>
        <Button type="normal" color="white" onClick={handleClearTags}>
          очистить все
        </Button>
        <Button type="normal" color="green" onClick={handleSaveTags}>
          сохранить
        </Button>
      </div>
    </Container>
  );
}
