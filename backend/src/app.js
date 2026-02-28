import express from "express";
import cors from "cors";
import { protectedRouter } from "./routes/protectedroutes.js";
import { errorMiddleware } from "./middlewares/middleware.js";
import { notebookRouter } from "./routes/notebookroutes.js";
import { documentRouter } from "./routes/documentroutes.js";
import { chunkRouter } from "./routes/chunkroutes.js";
import { searchRouter } from "./routes/searchroutes.js";
import { chatRouter } from "./routes/chatroutes.js";





const app = express();

app.use(cors());
app.use(express.json());



app.use("/protected", protectedRouter);
app.use("/notebooks", notebookRouter);
app.use("/documents", documentRouter);
app.use("/chunks", chunkRouter);
app.use("/search", searchRouter);
app.use("/chat", chatRouter);
app.use(errorMiddleware);

export default app;