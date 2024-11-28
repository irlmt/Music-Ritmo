import Image from "next/image";

import { Button } from "@/shared/button";
import { Input } from "@/shared/input";
import { Container } from "@/shared/container";
import { Logo } from "@/shared/logo";

export default function Home() {
  return (
    <>
      <Logo type="big" />
      <Container style={{ margin: "50px" }} direction="column">
        <h1>Добро пожаловать в musicRitmo!</h1>
        <h2>Добро пожаловать в musicRitmo!</h2>
        <p>Добро пожаловать в musicRitmo!</p>
        <i className="fa-regular fa-heart"></i>
        <Button type="normal" color="green" disabled={true}>
          вход
        </Button>
        <Button type="normal" color="white" disabled={true}>
          вход
        </Button>
        <Button type="transparent" color="green-text">
          вход
        </Button>
        <Input type="text" placeholder="введите пароль" />
      </Container>
    </>
  );
}
