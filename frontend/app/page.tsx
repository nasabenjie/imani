"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Supermarket = {
  id: number;
  name: string;
  location: string;
  image_url: string;
};

const STORE_EMOJIS = ["🏪", "🛍️", "🌿", "🏬", "🧺", "🥦"];

export default function Home() {
  const [supermarkets, setSupermarkets] = useState<Supermarket[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/supermarkets/`)
      .then(r => r.json())
      .then(data => { setSupermarkets(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <main className="page">

      {/* ── Hero ── */}
      <section style={{ marginBottom: "64px" }}>
        <p className="fade-up" style={{
          fontSize: "11px",
          fontWeight: 700,
          letterSpacing: "3.5px",
          textTransform: "uppercase",
          color: "var(--gold-dark)",
          marginBottom: "16px",
        }}>
          Fresh · Local · East Africa
        </p>

        <h1 className="display fade-up delay-1" style={{
          fontSize: "clamp(42px, 7vw, 76px)",
          color: "var(--green-deep)",
          marginBottom: "20px",
        }}>
          Your market,<br />
          <span style={{ color: "var(--gold)" }}>at your door.</span>
        </h1>

        <p className="fade-up delay-2" style={{
          color: "var(--muted)",
          fontSize: "16px",
          lineHeight: 1.75,
          maxWidth: "420px",
          marginBottom: "32px",
        }}>
          Shop fresh groceries from trusted supermarkets across Uganda, delivered straight to you.
         
        </p>
      </section>

      {/* ── Stores ── */}
      <p className="section-label">Available Stores</p>

      {loading ? (
        <div style={{ color: "var(--muted)", padding: "40px 0" }}>Loading stores...</div>
      ) : (
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
          gap: "20px",
        }}>
          {supermarkets.map((market, i) => (
            <Link
              key={market.id}
              href={`/supermarkets/${market.id}`}
              style={{ textDecoration: "none" }}
            >
              <article className="card fade-up" style={{ animationDelay: `${0.1 * i}s` }}>

                {/* Banner */}
                <div style={{
                  height: "140px",
                  background: "linear-gradient(135deg, var(--green-deep) 0%, var(--green-mid) 65%, #2E7A50 100%)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "56px",
                  overflow: "hidden",
                  position: "relative",
                }}>
                  {market.image_url?.startsWith("http") ? (
                    <img
                      src={market.image_url}
                      alt={market.name}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  ) : (
                    STORE_EMOJIS[i % STORE_EMOJIS.length]
                  )}

                  {/* Gold accent line */}
                  <div style={{
                    position: "absolute",
                    bottom: 0, left: 0, right: 0,
                    height: "3px",
                    background: "var(--gold)",
                  }} />
                </div>

                {/* Body */}
                <div style={{ padding: "20px 22px 24px" }}>
                  <h2 className="display" style={{
                    fontSize: "21px",
                    color: "var(--text)",
                    marginBottom: "6px",
                  }}>
                    {market.name}
                  </h2>
                  <p style={{
                    color: "var(--muted)",
                    fontSize: "13px",
                    marginBottom: "18px",
                  }}>
                    📍 {market.location}
                  </p>
                  <span className="btn-secondary">Shop now →</span>
                </div>
              </article>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
