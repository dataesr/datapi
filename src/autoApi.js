import express from "express";
import mongoose from "mongoose";

export default function createAutoApi(collectionName) {
  const router = express.Router();

  // Schéma flexible (accepte n'importe quelle structure)
  const schema = new mongoose.Schema({}, { strict: false, timestamps: true });

  // Évite de recompiler le modèle si déjà existant
  const Model = mongoose.models[collectionName] || mongoose.model(collectionName, schema, collectionName);

  // GET /api/:collection — liste tous les documents
  router.get("/", async (req, res) => {
    try {
      const { limit = 20, skip = 0, sort, ...rawFilters } = req.query;

      const query = Model.find(filters).skip(Number(skip)).limit(Number(limit));
      if (sort) query.sort(sort);

      const docs = await query;
      const total = await Model.countDocuments(filters);

      res.json({ total, data: docs });
    } catch (err) {
      console.error("[autoApi] error:", err.message);
      res.status(500).json({ error: err.message });
    }
  });

  return router;
}
