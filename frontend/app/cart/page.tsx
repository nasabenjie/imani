"use client";

import Link from "next/link";
import Image from "next/image";
import { useCart } from "@/context/CartContext";

export default function CartPage() {
  const { cart, removeFromCart, increaseQty, decreaseQty, getTotalPrice, getTotalItems } = useCart();

  if (cart.length === 0) {
    return (
      <main style={{
        maxWidth: "560px",
        margin: "80px auto",
        padding: "0 24px",
        textAlign: "center",
      }}>
        <div style={{ fontSize: "72px", marginBottom: "20px" }}>🛒</div>
        <h1 className="display" style={{
          fontSize: "36px",
          color: "var(--green-deep)",
          marginBottom: "10px",
        }}>
          Your cart is empty
        </h1>
        <p style={{ color: "var(--muted)", marginBottom: "36px", fontSize: "15px" }}>
          Add some items to get started.
        </p>
        <Link href="/" className="btn-primary">
          Browse Stores
        </Link>
      </main>
    );
  }

  return (
    <main style={{ maxWidth: "660px", margin: "0 auto", padding: "48px 24px" }}>

      {/* Header */}
      <h1 className="display" style={{
        fontSize: "40px",
        color: "var(--green-deep)",
        marginBottom: "6px",
      }}>
        Your Cart
      </h1>
      <p style={{ color: "var(--muted)", fontSize: "14px", marginBottom: "36px" }}>
        {getTotalItems()} item{getTotalItems() !== 1 ? "s" : ""}
      </p>

      {/* Items */}
      <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "36px" }}>
        {cart.map(item => (
          <div key={item.id} style={{
            background: "var(--white)",
            borderRadius: "var(--radius-md)",
            padding: "16px",
            display: "flex",
            alignItems: "center",
            gap: "16px",
            boxShadow: "var(--shadow-sm)",
          }}>
            {/* Thumb */}
            <div style={{
              width: "64px",
              height: "64px",
              borderRadius: "var(--radius-sm)",
              background: "var(--green-light)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "28px",
              flexShrink: 0,
              position: "relative",
              overflow: "hidden",
            }}>
              {item.image_url?.startsWith("http") ? (
                <Image src={item.image_url} alt={item.name} fill style={{ objectFit: "cover" }} />
              ) : "🛒"}
            </div>

            {/* Info */}
            <div style={{ flex: 1 }}>
              <h2 className="display" style={{ fontSize: "18px", marginBottom: "2px" }}>
                {item.name}
              </h2>
              <p style={{ color: "var(--muted)", fontSize: "13px" }}>
                UGX {item.price.toLocaleString()} each
              </p>

              {/* Qty */}
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginTop: "10px" }}>
                <button
                  onClick={() => decreaseQty(item.id)}
                  style={{
                    width: "30px", height: "30px",
                    borderRadius: "var(--radius-sm)",
                    border: "1.5px solid var(--border)",
                    background: "var(--white)",
                    fontWeight: 700, fontSize: "16px",
                    cursor: "pointer", color: "var(--text)",
                  }}
                >−</button>
                <span style={{ fontWeight: 700, minWidth: "20px", textAlign: "center" }}>
                  {item.quantity}
                </span>
                <button
                  onClick={() => increaseQty(item.id)}
                  style={{
                    width: "30px", height: "30px",
                    borderRadius: "var(--radius-sm)",
                    border: "1.5px solid var(--border)",
                    background: "var(--white)",
                    fontWeight: 700, fontSize: "16px",
                    cursor: "pointer", color: "var(--text)",
                  }}
                >+</button>
              </div>
            </div>

            {/* Subtotal */}
            <div style={{ textAlign: "right", flexShrink: 0 }}>
              <p style={{
                fontWeight: 700,
                fontSize: "15px",
                color: "var(--green-deep)",
                marginBottom: "8px",
              }}>
                UGX {(item.price * item.quantity).toLocaleString()}
              </p>
              <button
                onClick={() => removeFromCart(item.id)}
                style={{
                  background: "none",
                  border: "none",
                  color: "var(--red)",
                  fontSize: "12px",
                  fontWeight: 600,
                  cursor: "pointer",
                  fontFamily: "var(--font-body), sans-serif",
                }}
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Order summary */}
      <div style={{
        background: "var(--white)",
        borderRadius: "var(--radius-md)",
        padding: "24px",
        boxShadow: "var(--shadow-sm)",
      }}>
        <p style={{
          fontSize: "11px",
          fontWeight: 700,
          letterSpacing: "2px",
          textTransform: "uppercase",
          color: "var(--muted)",
          marginBottom: "16px",
        }}>
          Order Summary
        </p>

        <div style={{
          display: "flex",
          justifyContent: "space-between",
          paddingBottom: "16px",
          borderBottom: "1px solid var(--border)",
          marginBottom: "16px",
          color: "var(--muted)",
          fontSize: "14px",
        }}>
          <span>Subtotal ({getTotalItems()} items)</span>
          <span style={{ fontWeight: 600, color: "var(--text)" }}>
            UGX {getTotalPrice().toLocaleString()}
          </span>
        </div>

        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "24px",
        }}>
          <span className="display" style={{ fontSize: "22px", color: "var(--green-deep)" }}>
            Total
          </span>
          <span className="display" style={{ fontSize: "22px", color: "var(--gold-dark)" }}>
            UGX {getTotalPrice().toLocaleString()}
          </span>
        </div>

        <button
          onClick={() => alert("Checkout coming soon!")}
          style={{
            width: "100%",
            background: "var(--green-deep)",
            color: "var(--gold)",
            border: "none",
            borderRadius: "var(--radius-md)",
            padding: "16px",
            fontFamily: "var(--font-display), 'Cormorant Garamond', Georgia, serif",
            fontWeight: 700,
            fontSize: "20px",
            cursor: "pointer",
            letterSpacing: "0.5px",
            transition: "background 0.18s ease",
          }}
          onMouseEnter={e => (e.currentTarget.style.background = "var(--green-mid)")}
          onMouseLeave={e => (e.currentTarget.style.background = "var(--green-deep)")}
        >
          Proceed to Checkout →
        </button>
      </div>

      <Link href="/" style={{
        display: "block",
        textAlign: "center",
        marginTop: "20px",
        color: "var(--muted)",
        fontSize: "14px",
        textDecoration: "none",
      }}>
        ← Continue Shopping
      </Link>
    </main>
  );
}
