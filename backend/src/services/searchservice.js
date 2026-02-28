import { embeddings } from "../config/embeddings.js";
import { qdrant } from "../config/qdrant.js";

export async function searchChunks({ documentId, userId, query }) {
  const vector = await embeddings.embedQuery(query);

  const result = await qdrant.search(process.env.QDRANT_COLLECTION, {
    vector,
    limit: 5,
    filter: {
      must: [
        { key: "documentId", match: { value: documentId } },
        { key: "userId", match: { value: userId } }
      ]
    }
  });

  return result;
}