import Image from "next/image";
import Logo from "../../public/images/logo.svg";

export default function Home() {
  return (
    <div>
      <h1>Добро пожаловать в musicRitmo!</h1>
      <h2>Добро пожаловать в musicRitmo!</h2>
      <p>Добро пожаловать в musicRitmo!</p>
      <Image src={Logo} alt="Логотип musicRitmo" width={100} height={100} />
      <i className="fa-regular fa-heart"></i>
    </div>
  );
}
