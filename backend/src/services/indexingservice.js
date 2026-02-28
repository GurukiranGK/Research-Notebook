import { embeddings } from "../config/embeddings.js";
import { qdrant } from "../config/qdrant.js";
import {ensureCollection} from "./vectorservice.js"

export async function indexChunks({ chunks }) {
  await ensureCollection();  
  const vectors = await embeddings.embedDocuments(
    chunks.map(c => c.content)
  );
  console.log("Embedding length:", vectors[0]?.length);
  

  const points = chunks.map((chunk, i) => ({
    id: chunk.id,
    vector: vectors[i],
    payload: {
      documentId: chunk.documentId,
      userId: chunk.userId,
      order: chunk.order
    }
  }));

  await qdrant.upsert(process.env.QDRANT_COLLECTION, {
    points
  });

 
}