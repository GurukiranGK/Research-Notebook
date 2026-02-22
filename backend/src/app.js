import express from "express";
import cors from "cors";
import { healthRouter } from "./routes/routes.js";
import { errorMiddleware } from "./middlewares/middleware.js";

const app = express();

app.use(cors());
app.use(express.json());

app.use("/health", healthRouter);

app.use(errorMiddleware);

export default app;