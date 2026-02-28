import { prisma } from "../config/db.js";

export class DocumentRepository {
  create({ notebookId, userId, filename, content }) {
    return prisma.document.create({
      data: {
        notebookId,
        userId,
        filename,
        content
      }
    });
  }

  findByNotebook({ notebookId, userId }) {
    return prisma.document.findMany({
      where: { notebookId, userId },
      orderBy: { createdAt: "desc" }
    });
  }

  findById({ id, userId }) {
  return prisma.document.findFirst({
    where: { id, userId }
  });
}
}