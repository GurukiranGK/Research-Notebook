import { GoogleGenerativeAIEmbeddings } from "@langchain/google-genai";

if (!process.env.GEMINI_API_KEY) {
  throw new Error("❌ GEMINI_API_KEY is missing");
}

export const embeddings = new GoogleGenerativeAIEmbeddings({
  apiKey: process.env.GEMINI_API_KEY,   // 🔴 REQUIRED
  model: "models/gemini-embedding-001"   // 🔴 REQUIRED
});

export default embeddings;