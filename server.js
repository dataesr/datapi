import "dotenv/config";
import express from "express";
import mongoose from "mongoose";
import createAutoApi from "./src/autoApi.js";

const app = express();
app.use(express.json());

// Connexion MongoDB
mongoose.connect(process.env.MONGO_URI, { dbName: process.env.MONGO_DB_NAME });

app.use("/api/:collection", (req, res, next) => {
  createAutoApi(req.params.collection)(req, res, next);
});

app.listen(3000, () => console.log("API running on http://localhost:3000"));
