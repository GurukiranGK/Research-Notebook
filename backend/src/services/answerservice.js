import { llm } from "../config/llm.js";

export async function answerQuestion({ question, chunks }) {
  const context = chunks
    .map((c, i) => `Chunk ${i + 1}:\n${c.content}`)
    .join("\n\n");

  const prompt = `
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
${context}

Question:
${question}

Answer:
`;

  const response = await llm.invoke(prompt);
  return response.content;
}