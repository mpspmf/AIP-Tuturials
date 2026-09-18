import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AIP · Guia de comunicação e colaboração",
  description:
    "Consulte os procedimentos de comunicação e colaboração na AIP: Teams, calendários, Planner e envio de emails em série.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-PT">
      <body className="antialiased">{children}</body>
    </html>
  );
}
