export default {
  logger: {
    logLevel: process.env.LOG_LEVEL || "info",
  },
  mongo: {
    uri: process.env.MONGO_URI || "mongodb://localhost:27017/",
    dbName: process.env.MONGO_DB_NAME || "dataesr",
  },
  pipeline: {
    sourceCollection: process.env.SOURCE_COLLECTION || "ma_collection_source",
    targetCollection: process.env.TARGET_COLLECTION || "ma_collection_cible",
  },
  // Configuration par collection
  // genericRoute  : exposer /api/:collection (auto-API générique) et /doc:collection pour Swagger
  // customRoutes  : routes custom à documenter dans Swagger.
  // excluded      : bloquer complètement la collection (API + doc)
  collections: {
    atlas2023: {
      genericRoute: true,
      customRoutes: ["get-with-secret"],
    },
    boards: { excluded: true },
  },
};


