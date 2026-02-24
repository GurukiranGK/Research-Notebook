import express from "express";
import cors from "cors";
import { protectedRouter } from "./routes/protectedroutes.js";
import { errorMiddleware } from "./middlewares/middleware.js";
import { notebookRouter } from "./routes/notebookroutes.js";



const app = express();

app.use(cors());
app.use(express.json());


app.use("/protected", protectedRouter);
app.use("/notebooks", notebookRouter);
app.use(errorMiddleware);

export default app;