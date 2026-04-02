import "dotenv/config";

import { client } from "./src/services/mongo.js";
import { runPipeline } from "./src/pipeline.js";
import logger from "./src/services/logger.js";

try {
  await runPipeline();
} catch (e) {
  logger.error(`Erreur lors de l'exécution du pipeline: ${e.message}`, { stack: e.stack });
  process.exitCode = 1;
} finally {
  await client.close();
  logger.info("Connexion MongoDB fermée.");
}
