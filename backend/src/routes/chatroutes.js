import { Router } from "express";
import { keycloakAuth } from "../middlewares/keycloak.js";
import { chatWithDocument } from "../services/chatservice.js";

export const chatRouter = Router();

chatRouter.post("/", keycloakAuth, async (req, res) => {
  const { documentId, question } = req.body;

  if (!documentId || !question) {
    return res.status(400).json({ error: "documentId and question required" });
  }

  const result = await chatWithDocument({
    documentId,
    userId: req.user.id,
    question
  });

  res.json(result);
});