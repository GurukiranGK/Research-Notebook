import { Router } from "express";
import { keycloakAuth } from "../middlewares/keycloak.js";
import { DocumentRepository } from "../repositories/documentrepo.js";
import { chunkDocument } from "../services/chunkingservice.js";

export const chunkRouter = Router();
const docRepo = new DocumentRepository();

/**
 * Chunk a document
 */
chunkRouter.post("/:documentId", keycloakAuth, async (req, res) => {
  const document = await docRepo.findById({
    id: req.params.documentId,
    userId: req.user.id
  });

  if (!document) {
    return res.status(404).json({ error: "Document not found" });
  }

  const result = await chunkDocument({
    document,
    userId: req.user.id
  });

  res.json({
    message: "Document chunked",
    chunksCreated: result.count
  });
});