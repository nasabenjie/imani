"use client";

import { useCart } from "@/context/CartContext";
import Link from "next/link";

type AddToCartButtonProps = {
  productId: number;
};

export default function AddToCartButton({ productId }: AddToCartButtonProps) {

  const { cart, addToCart } = useCart();

  const isInCart = cart.some(item => item.id === productId);

  const handleAdd = () => {
    addToCart({
      id: productId,
      name: "Product",
      price: 0,
      image_url: ""
    });
  };

  if (isInCart) {
    return (
      <Link href="/cart">
        <button className="bg-blue-500 text-white px-3 py-1 rounded">
          Go to Cart
        </button>
      </Link>
    );
  }

  return (
    <button
      onClick={handleAdd}
      className="bg-green-500 text-white px-3 py-1 rounded"
    >
      Add to Cart
    </button>
  );
}