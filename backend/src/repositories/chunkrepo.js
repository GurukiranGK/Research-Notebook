import { prisma } from "../config/db.js";

export class ChunkRepository {
  async deleteByDocument({ documentId, userId }) {
    return prisma.chunk.deleteMany({
      where: { documentId, userId }
    });
  }

  async bulkCreate({ documentId, userId, chunks }) {
    return prisma.chunk.createMany({
      data: chunks.map(c => ({
        documentId,
        userId,
        content: c.content,
        order: c.order
      }))
    });
  }

  findByDocument({ documentId, userId }) {
    return prisma.chunk.findMany({
      where: { documentId, userId },
      orderBy: { order: "asc" }
    });
  }

  findByIds({ ids, userId }) {
  return prisma.chunk.findMany({
    where: {
      id: { in: ids },
      userId
    },
    orderBy: { order: "asc" }
  });
}
}