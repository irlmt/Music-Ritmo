"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import { Logo } from "@/shared/logo";

import styles from "./registration.module.css";

export default function Registration() {
  const router = useRouter();
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
          <Input type="text" placeholder="введите логин" maxLength={64} />
          <Input type="text" placeholder="введите пароль" maxLength={64} />
          <div className={styles.registration__content_button}>
            <Button
              type="normal"
              color="green"
              disabled={false}
              onClick={() => {
                router.push("/");
              }}
            >
              зарегистрироваться
            </Button>
          </div>
        </Container>
      </div>
    </div>
  );
}
