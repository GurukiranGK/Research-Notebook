import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

export const llm = new ChatGoogleGenerativeAI({
  model: "models/gemini-2.5-flash",
  apiKey: process.env.GEMINI_API_KEY,
  temperature: 0.2
});