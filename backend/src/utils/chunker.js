import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";
export async function chunkText(text) {
  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 500,
    chunkOverlap: 100,
    separators: ["\n\n", "\n", " ", ""]
  });

  const docs = await splitter.createDocuments([text]);

  return docs.map((doc, index) => ({
    content: doc.pageContent,
    order: index
  }));
}