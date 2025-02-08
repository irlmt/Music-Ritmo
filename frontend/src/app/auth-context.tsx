"use client";

import {
  createContext,
  useState,
  useEffect,
  useContext,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";

interface AuthContextType {
  user: string | null;
  password: string | null;
  login: (username: string, password: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const router = useRouter();
  const [user, setUser] = useState<string | null>(null);
  const [password, setPassword] = useState<string | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("username");
    const storedPassword = localStorage.getItem("password");
    if (storedUser && storedPassword) {
      setUser(storedUser);
      setPassword(storedPassword);
    } else {
      router.push("/login");
    }
  }, [router]);

  const login = (username: string, password: string) => {
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
    setUser(username);
    setPassword(password);
    router.push("/settings");
  };

  const logout = () => {
    localStorage.removeItem("username");
    localStorage.removeItem("password");
    setUser(null);
    setPassword(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, password, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
