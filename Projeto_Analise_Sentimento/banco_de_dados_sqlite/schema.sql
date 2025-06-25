CREATE TABLE "Aplicativos" (
    "id_app" INTEGER PRIMARY KEY AUTOINCREMENT,
    "nome" VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE "Reviews" (
    "id_review_sqlite" INTEGER PRIMARY KEY AUTOINCREMENT,
    "review_uuid" TEXT NOT NULL,
    "score" INTEGER,
    "id_app" INTEGER,
    FOREIGN KEY("id_app") REFERENCES "Aplicativos"("id_app")
); 