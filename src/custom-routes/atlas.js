import express from "express";
import mongoose from "mongoose";

const router = express.Router();

const schema = new mongoose.Schema({}, { strict: false, timestamps: true });
const getModel = (name) => mongoose.models[name] || mongoose.model(name, schema, name);

router.get("/:collection/get-with-secret", async (req, res) => {
  try {
    const { limit = 20, skip = 0, sort, ...filters } = req.query;
    const Model = getModel(req.params.collection);

    // Filtre avec secret: "non" et exclusion du champ secret des résultats
    const query = Model.find({ ...filters, secret: "non" }, { secret: 0 })
      .skip(Number(skip))
      .limit(Number(limit));
    if (sort) query.sort(sort);

    const docs = await query;
    const total = await Model.countDocuments({ ...filters, secret: "non" });

    res.json({ total, data: docs });
  } catch (err) {
    console.error("[get-with-secret] error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

export default router;
