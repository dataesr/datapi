import "dotenv/config";
import express from "express";
import mongoose from "mongoose";

import createAutoApi from "./src/autoApi.js";
import customRoutesAtlas from "./src/custom-routes/atlas.js";
import docApi from "./src/docApi.js";
import config from "./src/config.js";

const app = express();
app.use(express.json());

// Connexion MongoDB
mongoose.connect(process.env.MONGO_URI, { dbName: process.env.MONGO_DB_NAME });

// Documentation OpenAPI générée à la volée - json à passer à swagger-ui
app.use("/api", docApi);

// Swagger UI
app.get("/doc/:collection", (req, res) => {
  const { collection } = req.params;
  if (config.collections?.[collection]?.excluded) {
    return res.status(404).send("Not found");
  }
  // https://swagger.io/docs/open-source-tools/swagger-ui/usage/installation/#unpkg
  res.setHeader("Content-Type", "text/html");
  res.send(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <title>datapi — ${collection}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "/api/doc/${collection}",
      dom_id: "#swagger-ui",
      presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
      layout: "BaseLayout",
    });
  </script>
</body>
</html>`);
});

// Routes custom (avant l'auto-API pour prendre priorité)
app.use("/api", customRoutesAtlas);

// Auto-API générique — collections exclues ou sans genericRoute bloquées
app.use("/api/:collection", (req, res, next) => {
  const colConfig = config.collections?.[req.params.collection];
  if (colConfig?.excluded || colConfig?.genericRoute === false) {
    return res.status(404).json({ error: "Collection not found" });
  }
  createAutoApi(req.params.collection)(req, res, next);
});

app.listen(3000, () => console.log("API running on http://localhost:3000"));
