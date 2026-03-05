"use client";

import Link from "next/link";
import { useCart } from "@/context/CartContext";

export default function Navbar() {
  const { getTotalItems } = useCart();
  const totalItems = getTotalItems();

  return (
    <nav style={{
      background: "var(--green-deep)",
      height: "60px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 28px",
      position: "sticky",
      top: 0,
      zIndex: 100,
      boxShadow: "0 2px 16px rgba(0,0,0,0.20)",
    }}>
      <Link href="/" style={{ textDecoration: "none" }}>
        <span style={{
          fontFamily: "var(--font-display), 'Cormorant Garamond', Georgia, serif",
          fontWeight: 700,
          fontSize: "24px",
          color: "var(--gold)",
          letterSpacing: "2px",
          textTransform: "uppercase",
        }}>
          IMANI
        </span>
      </Link>

      <Link href="/cart" style={{ textDecoration: "none" }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          background: totalItems > 0 ? "var(--gold)" : "rgba(255,255,255,0.12)",
          color: totalItems > 0 ? "var(--green-deep)" : "rgba(255,255,255,0.85)",
          padding: "8px 20px",
          borderRadius: "var(--radius-full)",
          fontWeight: 700,
          fontSize: "14px",
          transition: "all 0.2s ease",
          fontFamily: "var(--font-body), sans-serif",
        }}>
          <span>🛒</span>
          <span>{totalItems > 0 ? `${totalItems} item${totalItems !== 1 ? "s" : ""}` : "Cart"}</span>
        </div>
      </Link>
    </nav>
  );
}
