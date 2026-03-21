import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Notion School Sync",
  description: "Notion <-> 1000.school sync control panel"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
