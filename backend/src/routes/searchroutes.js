import { Router } from "express";
import { keycloakAuth } from "../middlewares/keycloak.js";
import { searchChunks } from "../services/searchservice.js";

export const searchRouter = Router();

/**
 * Search chunks for a document
 */
searchRouter.post("/", keycloakAuth, async (req, res) => {
  const { documentId, query } = req.body;

  if (!documentId || !query) {
    return res.status(400).json({ error: "documentId and query are required" });
  }

  const results = await searchChunks({
    documentId,
    userId: req.user.id,
    query
  });

  res.json(results);
});