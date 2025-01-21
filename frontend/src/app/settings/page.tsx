"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import Image from "next/image";
import styles from "./settings.module.css";

export default function Settings() {
  const router = useRouter();
  return (
    <div className={styles.settings}>
      <div className={styles.settings__avatar}>
        <h1 className={styles.settings__avatar__name}>Иван Иванов</h1>
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
          <Input type="text" placeholder="введите логин" maxLength={64} />
          <Input
            type="password"
            placeholder="введите старый пароль"
            maxLength={64}
          />
          <Input
            type="password"
            placeholder="введите новый пароль"
            maxLength={64}
          />
          <Input
            type="password"
            placeholder="введите повторно новый пароль"
            maxLength={64}
          />
          <div className={styles.registration__content_button}>
            <Button
              type="normal"
              color="green"
              disabled={false}
              onClick={() => {
                router.push("/");
              }}
            >
              Сохранить изменения
            </Button>
          </div>
        </Container>
      </div>
    </div>
  );
}
