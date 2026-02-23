import jwt from "jsonwebtoken";
import jwksClient from "jwks-rsa";
import { env } from "../config/env.js";

const client = jwksClient({
  jwksUri: `${env.keycloakIssuer}/protocol/openid-connect/certs`
});

function getKey(header, callback) {
  client.getSigningKey(header.kid, function (err, key) {
    if (err) return callback(err);
    const signingKey = key.getPublicKey();
    callback(null, signingKey);
  });
}

export function keycloakAuth(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: "Missing Authorization header" });
  }

  const token = authHeader.split(" ")[1];

  jwt.verify(
    token,
    getKey,
    {
      issuer: env.keycloakIssuer
    },
    (err, decoded) => {
      if (err) {
        console.error("JWT error:", err.message);
        return res.status(401).json({ error: "Invalid token" });
      }

      req.user = {
        id: decoded.sub,
        username: decoded.preferred_username,
        email: decoded.email
      };

      next();
    }
  );
}