-- Syntax: SQLite3

PRAGMA foreign_key = ON;

ATTACH DATABASE "szemely.db" AS "Személy";
ATTACH DATABASE "szervezet.db" AS "Szervezet";

CREATE TABLE IF NOT EXISTS "Kontaktszemély" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid"),
    "szervezet" INTEGER REFERENCES "Szervezet"("rowid"),
    "beosztás" TEXT,
    "megjegyzés" TEXT
);
