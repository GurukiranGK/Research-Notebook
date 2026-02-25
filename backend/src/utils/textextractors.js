export async function extractText(file) {
  const mime = file.mimetype;

  // Plain text
  if (mime === "text/plain") {
    return file.buffer.toString("utf-8");
  }

  throw new Error("Unsupported file type");
}