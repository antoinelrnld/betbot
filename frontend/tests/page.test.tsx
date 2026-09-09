import type { AnchorHTMLAttributes, ReactNode } from "react";
import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";

vi.mock("next/link", () => ({
  default: ({
    children,
    ...props
  }: AnchorHTMLAttributes<HTMLAnchorElement> & { children?: ReactNode }) => (
    <a {...props}>{children}</a>
  ),
}));

import Home from "@/app/page";

test("renders the landing page for BetBot", () => {
  render(<Home />);

  expect(screen.getByRole("link", { name: "BetBot home" })).toHaveAttribute(
    "href",
    "/",
  );
  expect(
    screen.getByRole("heading", { name: /bet together/i }),
  ).toBeInTheDocument();
  expect(screen.getByText(/virtual currency only/i)).toBeInTheDocument();
});
