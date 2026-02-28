import { Router } from "express";
import { keycloakAuth } from "../middlewares/keycloak.js";
import { upload } from "../middlewares/uploadmiddleware.js";
import { extractText } from "../utils/textextractor.js";
import { DocumentRepository } from "../repositories/documentrepo.js";

export const documentRouter = Router();
const repo = new DocumentRepository();

/**
 * Upload document to notebook
 */
documentRouter.post(
  "/:notebookId",
  keycloakAuth,
  upload.single("file"),
  async (req, res) => {
    const text = await extractText(req.file);

    const doc = await repo.create({
      notebookId: req.params.notebookId,
      userId: req.user.id,
      filename: req.file.originalname,
      content: text
    });

    res.status(201).json(doc);
  }
);

/**
 * Get documents for notebook
 */
documentRouter.get("/:notebookId", keycloakAuth, async (req, res) => {
  const docs = await repo.findByNotebook({
    notebookId: req.params.notebookId,
    userId: req.user.id
  });

  res.json(docs);
});