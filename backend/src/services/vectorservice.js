import { qdrant } from "../config/qdrant.js";

export async function ensureCollection() {
  const collections = await qdrant.getCollections();

  const exists = collections.collections.some(
    c => c.name === process.env.QDRANT_COLLECTION
  );

  if (!exists) {
    await qdrant.createCollection(process.env.QDRANT_COLLECTION, {
      vectors: {
        size: 3072,        // ✅ Gemini embedding dimension
        distance: "Cosine"
      }
    });

    console.log("Qdrant collection created:", process.env.QDRANT_COLLECTION);
  } else {
    console.log("Qdrant collection already exists");
  }
}