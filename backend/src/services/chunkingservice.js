import { chunkText } from "../utils/chunker.js";
import { ChunkRepository } from "../repositories/chunkrepo.js";
import { indexChunks } from "./indexingservice.js";

const repo = new ChunkRepository();

export async function chunkDocument({ document, userId }) {
  // 1. Delete old chunks (safe re-run)
  await repo.deleteByDocument({
    documentId: document.id,
    userId
  });

  // 2. Create new chunks (LangChain)
  const chunks = await chunkText(document.content);
  console.log("Chunks:", chunks.length);
console.log("First chunk content:", JSON.stringify(chunks[0]?.content));
console.log("Content length:", chunks[0]?.content?.length);

  // 3. Store chunks in Postgres
  await repo.bulkCreate({
    documentId: document.id,
    userId,
    chunks
  });

  // 4. Fetch stored chunks (with IDs)
  const storedChunks = await repo.findByDocument({
    documentId: document.id,
    userId
  });

  // 5. Index chunks into Qdrant
  await indexChunks({ chunks: storedChunks });

  return { count: storedChunks.length };
}