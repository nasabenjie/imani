import { Supermarket } from "@/lib/types";

export default function SupermarketHeader({ supermarket }: { supermarket: Supermarket }) {
  const hasImage = supermarket.image_url?.startsWith("http");

  return (
    <div style={{ marginBottom: "36px" }}>
      {/* Banner */}
      <div style={{
        width: "100%",
        height: "200px",
        borderRadius: "var(--radius-lg)",
        overflow: "hidden",
        background: "linear-gradient(135deg, var(--green-deep) 0%, var(--green-mid) 60%, #2E7A50 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "80px",
        marginBottom: "24px",
        position: "relative",
      }}>
        {hasImage ? (
          <img
            src={supermarket.image_url}
            alt={supermarket.name}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : <span>🏪</span>}

        {/* Gold bottom accent */}
        <div style={{
          position: "absolute",
          bottom: 0, left: 0, right: 0,
          height: "4px",
          background: "var(--gold)",
        }} />

        {/* Location badge */}
        <div style={{
          position: "absolute",
          bottom: "18px",
          left: "20px",
          background: "rgba(26,58,42,0.75)",
          backdropFilter: "blur(8px)",
          color: "#fff",
          padding: "6px 14px",
          borderRadius: "var(--radius-full)",
          fontSize: "12px",
          fontWeight: 600,
          letterSpacing: "0.5px",
        }}>
          📍 {supermarket.location}
        </div>
      </div>

      <h1 className="display" style={{
        fontSize: "clamp(28px, 5vw, 40px)",
        color: "var(--green-deep)",
      }}>
        {supermarket.name}
      </h1>
    </div>
  );
}
