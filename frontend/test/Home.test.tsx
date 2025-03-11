import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import GenreList from "../src/app/page";
import "@testing-library/jest-dom";
import { useRouter } from "next/navigation";
import { AuthProvider } from "@/app/auth-context";

global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
  })
) as jest.Mock;

jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

const mockPush = jest.fn();
(useRouter as jest.Mock).mockReturnValue({
  push: mockPush,
});

describe("GenreList Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const renderWithAuthProvider = (component: React.ReactElement) => {
    return render(<AuthProvider>{component}</AuthProvider>);
  };

  test("shows loading state initially", () => {
    renderWithAuthProvider(<GenreList />);
    expect(screen.getByText("Загрузка...")).toBeInTheDocument();
  });

  test("shows error message when data fetching fails", async () => {
    global.fetch = jest.fn(() =>
      Promise.reject(new Error("Не удалось получить данные с сервера"))
    ) as jest.Mock;

    renderWithAuthProvider(<GenreList />);

    const errorMessage = await screen.findByText(/Ошибка:/);
    expect(errorMessage).toBeInTheDocument();
  });

  test("displays genres when data is fetched successfully", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            "subsonic-response": {
              status: "ok",
              genres: {
                genre: [
                  { value: "Rock", songCount: 100, albumCount: 10 },
                  { value: "Pop", songCount: 200, albumCount: 20 },
                ],
              },
            },
          }),
      })
    ) as jest.Mock;

    renderWithAuthProvider(<GenreList />);

    const rockGenre = await screen.findByText("Rock");
    const popGenre = await screen.findByText("Pop");
    expect(rockGenre).toBeInTheDocument();
    expect(popGenre).toBeInTheDocument();
  });

  test("displays message when no genres are available", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            "subsonic-response": {
              status: "ok",
              genres: {
                genre: [],
              },
            },
          }),
      })
    ) as jest.Mock;

    renderWithAuthProvider(<GenreList />);

    const noGenresMessage = await screen.findByText("Нет доступных жанров");
    expect(noGenresMessage).toBeInTheDocument();
  });

  test("navigates to media page when button is clicked", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            "subsonic-response": {
              status: "ok",
              genres: {
                genre: [{ value: "Rock", songCount: 100, albumCount: 10 }],
              },
            },
          }),
      })
    ) as jest.Mock;

    renderWithAuthProvider(<GenreList />);

    const mediaButton = await screen.findByText("медиатека");
    fireEvent.click(mediaButton);

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/media");
    });
  });
});
