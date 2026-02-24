import { Router } from "express";
import { keycloakAuth } from "../middlewares/keycloak.js";
import { NotebookRepository } from "../repositories/notebook.js";

export const notebookRouter = Router();
const repo = new NotebookRepository();

/**
 * Create notebook
 */
notebookRouter.post("/", keycloakAuth, async (req, res) => {
  const notebook = await repo.create({
    title: req.body.title,
    userId: req.user.id
  });
  res.status(201).json(notebook);
});

/**
 * Get my notebooks
 */
notebookRouter.get("/", keycloakAuth, async (req, res) => {
  const notebooks = await repo.findByUser(req.user.id);
  res.json(notebooks);
});

/**
 * Update notebook
 */
notebookRouter.put("/:id", keycloakAuth, async (req, res) => {
  const result = await repo.update({
    id: req.params.id,
    userId: req.user.id,
    title: req.body.title
  });

  if (result.count === 0) {
    return res.status(404).json({ error: "Notebook not found" });
  }

  res.json({ success: true });
});

/**
 * Delete notebook
 */
notebookRouter.delete("/:id", keycloakAuth, async (req, res) => {
  const result = await repo.delete({
    id: req.params.id,
    userId: req.user.id
  });

  if (result.count === 0) {
    return res.status(404).json({ error: "Notebook not found" });
  }

  res.json({ success: true });
});