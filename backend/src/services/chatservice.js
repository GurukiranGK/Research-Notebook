import { searchChunks } from "./searchservice.js";
import { ChunkRepository } from "../repositories/chunkrepo.js";
import { answerQuestion } from "./answerservice.js";

const chunkRepo = new ChunkRepository();

export async function chatWithDocument({ documentId, userId, question }) {
  // 1. Retrieve relevant chunks
  const results = await searchChunks({
    documentId,
    userId,
    query: question,
    limit: 5
  });

  const chunkIds = results.map(r => r.id);

  // 2. Fetch chunk text
  const chunks = await chunkRepo.findByIds({
    ids: chunkIds,
    userId
  });

  // 3. Generate answer
  const answer = await answerQuestion({
    question,
    chunks
  });

  return {
    answer,
    sources: chunkIds
  };
}