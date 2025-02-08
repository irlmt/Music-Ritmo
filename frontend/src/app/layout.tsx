import type { Metadata } from "next";
import { AuthProvider } from "./auth-context";

import "./globals.css";

export const metadata: Metadata = {
  title: "Music Ritmo",
  description: "Music streaming service",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <AuthProvider>
      <html lang="ru">
        <body>{children}</body>
      </html>
    </AuthProvider>
  );
}
