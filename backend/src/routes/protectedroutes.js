import { Router } from "express";
import { keycloakAuth } from "../middlewares/keycloak.js";

export const protectedRouter = Router();

protectedRouter.get("/", keycloakAuth, (req, res) => {
  res.json({
    message: "Protected route access granted",
    user: req.user
  });
});