"use client";

import { useEffect, useState, useMemo } from "react";
import { useParams } from "next/navigation";
import { Product, Supermarket } from "@/lib/types";
import ProductGrid from "@/components/product/ProductGrid";
import SupermarketHeader from "@/components/supermarket/SupermarketHeader";

export default function SupermarketPage() {
  const params = useParams();
  const supermarketId = params.id as string;

  const [supermarket, setSupermarket] = useState<Supermarket | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [smRes, prRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/supermarkets/${supermarketId}/`),
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/products/?supermarket=${supermarketId}`),
        ]);
        setSupermarket(await smRes.json());
        setProducts(await prRes.json());
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [supermarketId]);

  const categories = useMemo(() => {
    const unique = new Set(products.map(p => p.category_name));
    return ["All", ...Array.from(unique)];
  }, [products]);

  const filtered = useMemo(() =>
    selectedCategory === "All" ? products : products.filter(p => p.category_name === selectedCategory),
    [products, selectedCategory]
  );

  if (loading) return (
    <div className="page" style={{ color: "var(--muted)" }}>Loading store...</div>
  );

  if (!supermarket) return (
    <div className="page" style={{ color: "var(--red)" }}>Store not found.</div>
  );

  return (
    <div className="page">
      <SupermarketHeader supermarket={supermarket} />

      {/* Category filters */}
      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "12px" }}>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              padding: "7px 18px",
              borderRadius: "var(--radius-full)",
              border: selectedCategory === cat ? "none" : "1.5px solid var(--border)",
              background: selectedCategory === cat ? "var(--green-deep)" : "var(--white)",
              color: selectedCategory === cat ? "var(--gold)" : "var(--text)",
              fontWeight: 700,
              fontSize: "13px",
              cursor: "pointer",
              transition: "all 0.15s ease",
              fontFamily: "var(--font-body), sans-serif",
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      <p style={{ color: "var(--muted)", fontSize: "13px", marginBottom: "24px" }}>
        {filtered.length} product{filtered.length !== 1 ? "s" : ""}
        {selectedCategory !== "All" ? ` in ${selectedCategory}` : ""}
      </p>

      <ProductGrid products={filtered} />
    </div>
  );
}
