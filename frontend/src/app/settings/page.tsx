"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import Image from "next/image";
import { useAuth } from "@/app/auth-context";
import styles from "./settings.module.css";

export default function Settings() {
  const router = useRouter();
  const { user, login } = useAuth();
  const [newUsername, setNewUsername] = useState<string>("");
  const [, setPassword] = useState<string>("");
  const [newPassword, setNewPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");

  const updateUsername = async () => {
    if (!newUsername) {
      setErrorMessage("Пожалуйста, введите новый логин.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setErrorMessage("Пароли не совпадают.");
      return;
    }

    if (!user) {
      setErrorMessage("Вы не авторизованы.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/rest/updateUser?username=${newUsername}&u=${user}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
        }
      );

      const data = await response.json();
      if (data["subsonic-response"]?.status === "ok") {
        setErrorMessage("");
        setNewUsername("");
        setPassword("");
        setNewPassword("");
        setConfirmPassword("");
        login(newUsername);
      } else {
        setErrorMessage("Ошибка при изменении логина.");
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(`Ошибка сети: ${err.message}`);
      } else {
        setErrorMessage("Неизвестная ошибка.");
      }
    }
  };

  return (
    <div className={styles.settings}>
      <div className={styles.settings__avatar}>
        <h1 className={styles.settings__avatar__name}>{user}</h1>
        <Image
          src="/images/logo.svg"
          alt="User Avatar"
          width={300}
          height={300}
          className={styles.settings__avatar__image}
        />
        <Button
          type="normal"
          color="white"
          disabled={false}
          onClick={() => {
            router.push("/");
          }}
        >
          Сменить аватар
        </Button>
        <Button
          type="normal"
          color="green"
          disabled={false}
          onClick={() => {
            router.push("/");
          }}
        >
          Сохранить аватар
        </Button>
      </div>
      <div className={styles.settings__content}>
        <Container
          style={{ height: "45vh", width: "30vw" }}
          direction="column"
          arrow={true}
          link_arrow="/login"
        >
          <h2 className={styles.registration__content__title}>Смена логина</h2>
          <Input
            type="text"
            placeholder="введите логин"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
          <Input
            type="password"
            placeholder="введите новый пароль"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          {errorMessage && <div className={styles.error}>{errorMessage}</div>}
          <div className={styles.registration__content_button}>
            <Button
              type="normal"
              color="green"
              disabled={false}
              onClick={updateUsername}
            >
              Сохранить изменения
            </Button>
          </div>
        </Container>
      </div>
    </div>
  );
}
