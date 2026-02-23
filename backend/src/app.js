import express from "express";
import cors from "cors";
import { protectedRouter } from "./routes/protectedroutes.js";
import { errorMiddleware } from "./middlewares/middleware.js";

const app = express();

app.use(cors());
app.use(express.json());


app.use("/protected", protectedRouter);

app.use(errorMiddleware);

export default app;