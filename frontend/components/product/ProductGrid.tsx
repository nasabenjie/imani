import ProductCard from "./ProductCard";
import { Product } from "@/lib/types";

export default function ProductGrid({
  products,
}: {
  products: Product[];
}) {

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

      {products.map(product => (

        <ProductCard
          key={product.id}
          product={product}
        />

      ))}

    </div>
  );
}