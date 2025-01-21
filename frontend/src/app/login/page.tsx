"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import { Logo } from "@/shared/logo";

import styles from "./login.module.css";

export default function Login() {
  const router = useRouter();
  return (
    <div className={styles.login}>
      <div className={styles.login__logo}>
        <Logo type="big" />
      </div>
      <div className={styles.login__content}>
        <Container style={{ height: "35vh", width: "28vw" }} direction="column">
          <h2 className={styles.login__content__title}>Вход</h2>
          <Input type="text" placeholder="введите логин" />
          <Input type="text" placeholder="введите пароль" />
          <div className={styles.login__content_button}>
            <Button
              type="normal"
              color="green"
              disabled={false}
              onClick={() => {
                router.push("/");
              }}
            >
              войти
            </Button>
          </div>
        </Container>
        <Button
          type="transparent"
          color="green-text"
          onClick={() => {
            router.push("/registration");
          }}
        >
          регистрация
        </Button>
      </div>
    </div>
  );
}
