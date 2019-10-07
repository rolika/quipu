-- Syntax: SQLite3

PRAGMA foreign_keys = ON;

ATTACH DATABASE "szemely.db" AS "Személy";
ATTACH DATABASE "szervezet.db" AS "Szervezet";
ATTACH DATABASE "munka.db" AS "Munka";

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "KontaktSzemély" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"."Személy"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "szervezet" INTEGER REFERENCES "Szervezet"."Szervezet"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "megjegyzés" TEXT
);

-- évente új táblázat készül az ajánlatoknak
CREATE TABLE IF NOT EXISTS "Árajánlat2019" (
    "szám" TEXT PRIMARY KEY,
    "munkarész" INTEGER NOT NULL REFERENCES "Munka"."Munkarész"("rowid") ON DELETE RESTRICT ON UPDATE RESTRICT,
    "kontaktszemély" INTEGER REFERENCES "Kontaktszemély"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "témafelelős" INTEGER REFERENCES "Kontaktszemély"("rowid") ON DELETE RESTRICT ON UPDATE CASCADE,
    "érkezett" DATE DEFAULT (date('now')),
    "leadási határidő" DATE DEFAULT (date('now', '+1 week')),
    "leadva" DATE,
    "érvényes" DATE,
    "ajánlati ár" INTEGER,
    "esély" INTEGER DEFAULT 5, -- <100%: esély, 100%: nyert,
    "megjegyzés" TEXT
);
