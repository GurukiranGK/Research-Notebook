import { prisma } from "../config/db.js";

export class NotebookRepository {
  create({ title, userId }) {
    return prisma.notebook.create({
      data: { title, userId }
    });
  }

  findByUser(userId) {
    return prisma.notebook.findMany({
      where: { userId },
      orderBy: { createdAt: "desc" }
    });
  }

  findById({ id, userId }) {
    return prisma.notebook.findFirst({
      where: { id, userId }
    });
  }

  update({ id, userId, title }) {
    return prisma.notebook.updateMany({
      where: { id, userId },
      data: { title }
    });
  }

  delete({ id, userId }) {
    return prisma.notebook.deleteMany({
      where: { id, userId }
    });
  }
}