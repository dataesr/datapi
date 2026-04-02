import { MongoClient } from "mongodb";

import config from "../config.js";
import logger from "./logger.js";

const { uri, dbName } = config.mongo;

const client = new MongoClient(uri);

logger.info(`Connexion à MongoDB... ${uri}`);
await client.connect().catch((e) => {
  logger.error(`Échec de la connexion MongoDB: ${e.message}`);
  process.kill(process.pid, "SIGTERM");
});

logger.info(`Connecté à la base de données: ${dbName}`);
const db = client.db(dbName);

export { client, db };
