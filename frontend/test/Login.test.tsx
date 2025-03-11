import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Login from "@/app/login/page";
import { useRouter } from "next/navigation";
import { useAuth } from "@/app/auth-context";

jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

jest.mock("../src/app/auth-context", () => ({
  useAuth: jest.fn(),
}));

describe("Login Component", () => {
  const mockPush = jest.fn();
  const mockLogin = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    });
    (useAuth as jest.Mock).mockReturnValue({
      login: mockLogin,
    });
  });

  test("validates username and password length", () => {
    render(<Login />);

    const usernameInput = screen.getByPlaceholderText("введите логин");
    const passwordInput = screen.getByPlaceholderText("введите пароль");

    fireEvent.change(usernameInput, { target: { value: "12345" } });
    fireEvent.change(passwordInput, { target: { value: "12345" } });
    expect(
      screen.queryByText("Логин должен быть от 5 до 64 символов.")
    ).toBeNull();
    expect(
      screen.queryByText("Пароль должен быть от 5 до 64 символов.")
    ).toBeNull();

    const longValue = "a".repeat(64);
    fireEvent.change(usernameInput, { target: { value: longValue } });
    fireEvent.change(passwordInput, { target: { value: longValue } });
    expect(
      screen.queryByText("Логин должен быть от 5 до 64 символов.")
    ).toBeNull();
    expect(
      screen.queryByText("Пароль должен быть от 5 до 64 символов.")
    ).toBeNull();

    fireEvent.change(usernameInput, { target: { value: "1234" } });
    fireEvent.change(passwordInput, { target: { value: "1234" } });
    expect(
      screen.getByText("Логин должен быть от 5 до 64 символов.")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Пароль должен быть от 5 до 64 символов.")
    ).toBeInTheDocument();

    const tooLongValue = "a".repeat(65);
    fireEvent.change(usernameInput, { target: { value: tooLongValue } });
    fireEvent.change(passwordInput, { target: { value: tooLongValue } });
    expect(
      screen.getByText("Логин должен быть от 5 до 64 символов.")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Пароль должен быть от 5 до 64 символов.")
    ).toBeInTheDocument();
  });

  test.each([
    [
      "validuser",
      "validpassword",
      true,
      "Корректный логин + корректный пароль",
    ],
    ["validuser", "short", false, "Корректный логин + некорректный пароль"],
    [
      "invaliduser",
      "validpassword",
      false,
      "Некорректный логин + корректный пароль",
    ],
    ["invaliduser", "short", false, "Некорректный логин + некорректный пароль"],
  ])(
    "Тестирование комбинации логин и пароль: ",
    async (username, password, isSuccess) => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          status: isSuccess ? 200 : 400,
          json: () =>
            Promise.resolve(
              isSuccess
                ? { "subsonic-response": { status: "ok", user: {} } }
                : { "subsonic-response": { status: "error" } }
            ),
        })
      ) as jest.Mock;

      render(<Login />);

      const usernameInput = screen.getByPlaceholderText("введите логин");
      const passwordInput = screen.getByPlaceholderText("введите пароль");
      const loginButton = screen.getByText("Войти");

      fireEvent.change(usernameInput, { target: { value: username } });
      fireEvent.change(passwordInput, { target: { value: password } });
      fireEvent.click(loginButton);

      if (isSuccess) {
        await waitFor(() => {
          expect(mockLogin).toHaveBeenCalledWith(username, password);
        });
        await waitFor(() => {
          expect(mockPush).toHaveBeenCalledWith("/");
        });
      } else {
        if (username.length < 5 || username.length > 64) {
          expect(
            screen.getByText("Логин должен быть от 5 до 64 символов.")
          ).toBeInTheDocument();
        }
        if (password.length < 5 || password.length > 64) {
          expect(
            screen.getByText("Пароль должен быть от 5 до 64 символов.")
          ).toBeInTheDocument();
        }
      }
    }
  );

  test("displays error message for empty fields", () => {
    render(<Login />);

    const submitButton = screen.getByText("Войти");
    fireEvent.click(submitButton);

    expect(
      screen.getByText("Пожалуйста, заполните все поля.")
    ).toBeInTheDocument();
  });

  test("renders login form correctly", () => {
    render(<Login />);

    expect(screen.getByPlaceholderText("введите логин")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("введите пароль")).toBeInTheDocument();
    expect(screen.getByText("Войти")).toBeInTheDocument();
    expect(screen.getByText("регистрация")).toBeInTheDocument();
  });
});
