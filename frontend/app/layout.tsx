import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BetBot | Virtual betting for Discord communities",
  description:
    "BetBot is a Discord-first virtual betting platform. The web experience is coming soon.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
