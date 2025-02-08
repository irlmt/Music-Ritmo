"use client";

import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import { Logo } from "@/shared/logo";
import styles from "./registration.module.css";

export default function Registration() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [usernameError, setUsernameError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validateFields = () => {
    if (!username || !password) {
      setErrorMessage("Пожалуйста, заполните все поля.");
    } else {
      setErrorMessage("");
    }
  };

  const validateUsername = (value: string) => {
    if (!value) {
      setUsernameError("Пожалуйста, введите логин.");
    } else if (value.length < 5 || value.length > 64) {
      setUsernameError("Логин должен быть от 5 до 64 символов.");
    } else {
      setUsernameError("");
    }
  };

  const validatePassword = (value: string) => {
    if (!value) {
      setPasswordError("Пожалуйста, введите пароль.");
    } else if (value.length < 5 || value.length > 64) {
      setPasswordError("Пароль должен быть от 5 до 64 символов.");
    } else {
      setPasswordError("");
    }
  };

  useEffect(() => {
    validateFields();
  }, []);

  const handleSubmit = async () => {
    if (usernameError || passwordError || !username || !password) {
      setErrorMessage("Пожалуйста, исправьте все ошибки.");
      return;
    }

    setLoading(true);
    setErrorMessage("");
    setSuccessMessage("");

    try {
      const response = await fetch(
        `http://localhost:8000/rest/createUser?username=${username}&password=${password}&email=defemail@gmail.com}`,
        {
          method: "GET",
        }
      );

      const data = await response.json();

      if (data["subsonic-response"]?.status === "ok") {
        setSuccessMessage("Вы успешно зарегистрированы!");
        setTimeout(() => {
          router.push("/");
        }, 2000);
      } else {
        setErrorMessage("Ошибка при регистрации. Попробуйте снова.");
      }
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setErrorMessage("Ошибка сети. Пожалуйста, попробуйте позже.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.registration}>
      <div className={styles.registration__logo}>
        <Logo type="big" />
      </div>
      <div className={styles.registration__content}>
        <Container
          style={{ height: "35vh", width: "28vw" }}
          direction="column"
          arrow={true}
          link_arrow="/login"
        >
          <h2 className={styles.registration__content__title}>Регистрация</h2>
          <Input
            type="text"
            placeholder="введите логин"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              validateUsername(e.target.value);
              validateFields();
            }}
          />
          {usernameError && <div className={styles.error}>{usernameError}</div>}

          <Input
            type="password"
            placeholder="введите пароль"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              validatePassword(e.target.value);
              validateFields();
            }}
          />
          {passwordError && <div className={styles.error}>{passwordError}</div>}
          {errorMessage && <div className={styles.error}>{errorMessage}</div>}
          {successMessage && (
            <div className={styles.success}>{successMessage}</div>
          )}

          <div className={styles.registration__content_button}>
            <Button
              type="normal"
              color="green"
              disabled={Boolean(
                loading ||
                  usernameError ||
                  passwordError ||
                  !username ||
                  !password
              )}
              onClick={handleSubmit}
            >
              {loading ? "Загружается..." : "Зарегистрироваться"}
            </Button>
          </div>
        </Container>
      </div>
    </div>
  );
}
