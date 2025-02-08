"use client";

import { useState, useEffect, useCallback } from "react";
import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import { useAuth } from "@/app/auth-context";
import Image from "next/image";
import styles from "./settings.module.css";

export default function Settings() {
  const { user, password, login } = useAuth();
  const [newUsername, setNewUsername] = useState<string>(user || "");
  const [newPassword, setNewPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [, setErrorMessage] = useState<string>("");
  const [isUsernameUnique, setIsUsernameUnique] = useState<boolean>(true);

  const checkUsernameUniqueness = useCallback(
    async (username: string) => {
      const response = await fetch(
        `http://localhost:8000/rest/getUsers?username=${user}&u=${user}&p=${password}`
      );
      const data = await response.json();

      if (data["subsonic-response"]?.status === "ok") {
        const existingUsernames = data["subsonic-response"].users.user.map(
          (user: { username: string }) => user.username
        );
        setIsUsernameUnique(!existingUsernames.includes(username));
      } else {
        setErrorMessage("Ошибка при проверке пользователей.");
      }
    },
    [user, password]
  );

  const updateUsername = async () => {
    if (!newUsername) {
      setErrorMessage("Пожалуйста, введите новый логин.");
      return;
    }

    if (!isUsernameUnique) {
      setErrorMessage("Этот логин уже занят.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setErrorMessage("Пароли не совпадают.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/rest/updateUser?username=${user}&u=${user}&p=${password}&newUsername=${newUsername}`,
        {
          method: "GET",
        }
      );

      const data = await response.json();
      if (data["subsonic-response"]?.status === "ok") {
        setErrorMessage("");
        setNewPassword("");
        setConfirmPassword("");

        login(newUsername, newPassword);
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

  const changePassword = async () => {
    if (newPassword !== confirmPassword) {
      setErrorMessage("Пароли не совпадают.");
      return;
    }

    if (!newPassword || !confirmPassword) {
      setErrorMessage("Пожалуйста, введите новый пароль.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/rest/changePassword?username=${user}&u=${user}&p=${password}&password=${newPassword}`,
        {
          method: "GET",
        }
      );

      const data = await response.json();
      if (data["subsonic-response"]?.status === "ok") {
        setErrorMessage("");
        setNewPassword("");
        setConfirmPassword("");
      } else {
        setErrorMessage("Ошибка при изменении пароля.");
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(`Ошибка сети: ${err.message}`);
      } else {
        setErrorMessage("Неизвестная ошибка.");
      }
    }
  };
  useEffect(() => {
    if (newUsername) {
      checkUsernameUniqueness(newUsername);
    }
  }, [newUsername, checkUsernameUniqueness]);

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
            placeholder="введите новый логин"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
          {!isUsernameUnique && (
            <div className={styles.errorMessage}>Этот логин уже занят.</div>
          )}
          <Input
            type="password"
            placeholder="введите новый пароль"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <Input
            type="password"
            placeholder="подтвердите новый пароль"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {newPassword !== confirmPassword && (
            <div className={styles.errorMessage}>Пароли не совпадают.</div>
          )}
          {(!newUsername || !newPassword || !confirmPassword) && (
            <div className={styles.errorMessage}>
              Пожалуйста, заполните все поля.
            </div>
          )}
          <div className={styles.registration__content_button}>
            <Button
              type="normal"
              color="green"
              disabled={false}
              onClick={updateUsername}
            >
              Сохранить изменения логина
            </Button>
            <Button
              type="normal"
              color="green"
              disabled={false}
              onClick={changePassword}
            >
              Сохранить изменения пароля
            </Button>
          </div>
        </Container>
      </div>
    </div>
  );
}
