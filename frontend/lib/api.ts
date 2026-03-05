const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function getSupermarkets() {
  const res = await fetch(`${BASE_URL}/api/supermarkets/`);
  return res.json();
}

export async function getSupermarket(id: string) {
  const res = await fetch(`${BASE_URL}/api/supermarkets/${id}/`);
  return res.json();
}

export async function getProducts(supermarketId: string) {
  const res = await fetch(`${BASE_URL}/api/products/?supermarket=${supermarketId}`);
  return res.json();
}