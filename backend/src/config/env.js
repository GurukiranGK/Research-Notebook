import dotenv from "dotenv";
dotenv.config();

export const env = {
  port: process.env.PORT || 4000,

  // Keycloak
  keycloakIssuer: process.env.KEYCLOAK_ISSUER,
  keycloakAudience: process.env.KEYCLOAK_AUDIENCE
};