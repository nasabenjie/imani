"use client";

import Image from "next/image";
import Link from "next/link";
import { useCart } from "@/context/CartContext";
import { Product } from "@/lib/types";

export default function ProductCard({ product }: { product: Product }) {
  const { cart, addToCart } = useCart();
  const isInCart = cart.some(item => item.id === product.id);
  const hasImage = product.image_url?.startsWith("http");

  return (
    <article style={{
      background: "var(--white)",
      borderRadius: "var(--radius-md)",
      overflow: "hidden",
      boxShadow: "var(--shadow-sm)",
      transition: "transform 0.2s ease, box-shadow 0.2s ease",
      display: "flex",
      flexDirection: "column",
    }}
      onMouseEnter={e => {
        (e.currentTarget as HTMLElement).style.transform = "translateY(-3px)";
        (e.currentTarget as HTMLElement).style.boxShadow = "var(--shadow-md)";
      }}
      onMouseLeave={e => {
        (e.currentTarget as HTMLElement).style.transform = "translateY(0)";
        (e.currentTarget as HTMLElement).style.boxShadow = "var(--shadow-sm)";
      }}
    >
      {/* Image */}
      <div style={{
        height: "130px",
        background: "var(--green-light)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "44px",
        position: "relative",
        overflow: "hidden",
      }}>
        {hasImage ? (
          <Image src={product.image_url} alt={product.name} fill style={{ objectFit: "cover" }} />
        ) : <span>🛒</span>}
      </div>

      {/* Body */}
      <div style={{
        padding: "12px 14px 16px",
        flex: 1,
        display: "flex",
        flexDirection: "column",
      }}>
        <span style={{
          fontSize: "10px",
          fontWeight: 700,
          letterSpacing: "1.5px",
          textTransform: "uppercase",
          color: "var(--gold-dark)",
          marginBottom: "4px",
        }}>
          {product.category_name}
        </span>

        <h2 className="display" style={{
          fontSize: "17px",
          color: "var(--text)",
          marginBottom: "6px",
          lineHeight: 1.3,
        }}>
          {product.name}
        </h2>

        <p style={{
          color: "var(--green-deep)",
          fontWeight: 700,
          fontSize: "15px",
          marginBottom: "14px",
        }}>
          UGX {parseFloat(product.price).toLocaleString()}
        </p>

        {isInCart ? (
          <Link href="/cart" style={{ textDecoration: "none", marginTop: "auto" }}>
            <button style={{
              width: "100%",
              background: "var(--gold)",
              color: "var(--green-deep)",
              border: "none",
              borderRadius: "var(--radius-sm)",
              padding: "10px 0",
              fontWeight: 700,
              fontSize: "13px",
              cursor: "pointer",
              fontFamily: "var(--font-body), sans-serif",
            }}>
              View Cart →
            </button>
          </Link>
        ) : (
          <button
            onClick={() => addToCart(product)}
            style={{
              width: "100%",
              background: "var(--green-deep)",
              color: "var(--gold)",
              border: "none",
              borderRadius: "var(--radius-sm)",
              padding: "10px 0",
              fontWeight: 700,
              fontSize: "13px",
              cursor: "pointer",
              marginTop: "auto",
              transition: "background 0.15s ease",
              fontFamily: "var(--font-body), sans-serif",
            }}
            onMouseEnter={e => (e.currentTarget.style.background = "var(--green-mid)")}
            onMouseLeave={e => (e.currentTarget.style.background = "var(--green-deep)")}
          >
            + Add to Cart
          </button>
        )}
      </div>
    </article>
  );
}
