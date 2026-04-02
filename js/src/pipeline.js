import { db } from "./services/mongo.js";
import config from "./config.js";
import logger from "./services/logger.js";

const { targetCollection } = config.pipeline;

function filterDocument(doc) {
  return doc.secret === "non";
}

function cleanDocument(doc) {
  // Supprimer l'_id pour éviter les conflits lors de l'insertion
  const { _id, ...rest } = doc;
  return rest;
}

export async function runPipeline() {
  logger.info("Lecture de la collection source : atlas2023");
  console.time("start");
  const allDocuments = await db.collection("atlas2023").find({}).toArray();
  console.timeEnd("start");
  logger.info(`${allDocuments.length} documents lus.`);
  console.time("filter");
  const filteredDocuments = allDocuments.filter(filterDocument); //.map(cleanDocument);
  console.timeEnd("filter");
  logger.info(`${filteredDocuments.length} documents retenus après filtrage`);

  if (filteredDocuments.length === 0) {
    logger.warn("Aucun document à insérer. Pipeline terminé.");
    return;
  }

  logger.info("Écriture dans la collection cible : atlas2023-jerem");
  // Vider la collection cible avant d'insérer (comportement par défaut : remplacement complet)
  await db.collection("atlas2023-jerem").deleteMany({});

  const result = await db.collection("atlas2023-jerem").insertMany(filteredDocuments);
  logger.info(`${result.insertedCount} documents insérés dans atlas2023-jerem`);
}
