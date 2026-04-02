import express from "express";
import mongoose from "mongoose";
import config from "./config.js";

const router = express.Router();

const schema = new mongoose.Schema({}, { strict: false });
const getModel = (name) => mongoose.models[name] || mongoose.model(name, schema, name);

// Infère un type OpenAPI à partir d'une valeur testée
function inferType(value) {
  if (value === null || value === undefined) return { type: "string", nullable: true };
  if (typeof value === "boolean") return { type: "boolean" };
  if (typeof value === "number") return Number.isInteger(value) ? { type: "integer" } : { type: "number" };
  if (value instanceof Date) return { type: "string", format: "date-time" };
  if (Array.isArray(value)) {
    const itemType = value.length > 0 ? inferType(value[0]) : { type: "string" };
    return { type: "array", items: itemType };
  }
  if (typeof value === "object") return { type: "object" };

  return { type: "string" };
}

// Construit un objet "properties" OpenAPI en fusionnant N documents
function inferProperties(docs) {
  const properties = {};
  for (const doc of docs) {
    const plain = doc.toObject ? doc.toObject() : doc;
    for (const [key, value] of Object.entries(plain)) {
      // Suppression des champs techniques MongoDB
      if (key === "_id") continue;
      if (key === "__v") continue;

      if (!properties[key]) {
        properties[key] = inferType(value);
      }
    }
  }
  return properties;
}

// GET /api/doc/:collection — spec OpenAPI générée à la volée
router.get("/doc/:collection", async (req, res) => {
  const { collection } = req.params;

  if (config.collections?.[collection]?.excluded) {
    return res.status(404).json({ error: "Collection not found" });
  }

  try {
    const Model = getModel(collection);
    const sample = await Model.find({}).limit(20);
    const properties = inferProperties(sample);
    const collectionConfig = config.collections?.[collection] ?? { genericRoute: true, customRoutes: [] };
    const paths = {};

    // Route générique - https://spec.openapis.org/oas/v3.0.0.html#paths-object
    if (collectionConfig.genericRoute) {
      paths[`/api/${collection}`] = {
        get: {
          summary: `Lister les documents de ${collection}`,
          parameters: [
            { name: "limit", in: "query", schema: { type: "integer", default: 20 } },
            { name: "skip", in: "query", schema: { type: "integer", default: 0 } },
            { name: "sort", in: "query", schema: { type: "string" }, description: "Ex: -annee-universitaire" },
            ...Object.keys(properties).map((field) => ({
              name: field,
              in: "query",
              schema: { type: properties[field].type || "string" },
              description: `Filtrer par ${field}`,
            })),
          ],
          responses: {
            200: {
              description: "Liste de documents",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      total: { type: "integer" },
                      data: { type: "array", items: { type: "object", properties } },
                    },
                  },
                },
              },
            },
          },
        },
      };
    }

    // Routes custom connues
    const customRouteDefs = {
      "get-without-secret": {
        // idem route generique mais filtre avec secret = "non" et exclusion du champ secret des résultats
        path: `/api/${collection}/get-without-secret`,
        spec: {
          get: {
            summary: `Lister les documents non-secrets de ${collection}`,
            // description: "Force `secret=non` et retire le champ `secret` du retour.",
            parameters: [
              { name: "limit", in: "query", schema: { type: "integer", default: 20 } },
              { name: "skip", in: "query", schema: { type: "integer", default: 0 } },
              { name: "sort", in: "query", schema: { type: "string" } },
              ...Object.keys(properties)
                .filter((field) => field !== "secret")
                .map((field) => ({
                  name: field,
                  in: "query",
                  schema: { type: properties[field].type || "string" },
                })),
            ],
            responses: {
              200: {
                description: "Liste de documents",
                content: {
                  "application/json": {
                    schema: {
                      type: "object",
                      properties: {
                        total: { type: "integer" },
                        data: {
                          type: "array",
                          items: {
                            type: "object",
                            properties: Object.fromEntries(Object.entries(properties).filter(([k]) => k !== "secret")),
                          },
                        },
                      },
                    },
                  },
                },
              },
            },
          },
        },
      },
    };

    // Ajout des routes custom à paths si déclarées dans config
    for (const routeName of collectionConfig.customRoutes ?? []) {
      const def = customRouteDefs[routeName];
      if (def) paths[def.path] = def.spec;
    }

    const spec = {
      openapi: "3.0.0",
      info: {
        title: `datapi — ${collection}`,
        version: "1.0.0",
        description: `Documentation générée automatiquement à partir d'un échantillon de 20 documents de la collection **${collection}**.`,
      },
      paths,
    };

    res.json(spec);
  } catch (err) {
    console.error("[docApi] error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

export default router;
