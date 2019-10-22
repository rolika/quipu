-- Syntax: SQLite3

PRAGMA foreign_keys = ON;

ATTACH DATABASE "kontaktszemely.db" AS "Kontaktszemély";
ATTACH DATABASE "munka.db" AS "Munka";

CREATE TABLE IF NOT EXISTS "Ajánlatkérés" (
    "munkarész" INTEGER NOT NULL REFERENCES "Munkarész"("rowid") ON DELETE RESTRICT ON UPDATE RESTRICT,
    "kontaktszemély" INTEGER REFERENCES "Kontaktszemély"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "témafelelős" INTEGER REFERENCES "Kontaktszemély"("rowid") ON DELETE RESTRICT ON UPDATE CASCADE,
    "érkezett" DATE DEFAULT (date('now')),
    "leadási határidő" DATE DEFAULT (date('now', '+1 week')),
    "megjegyzés" TEXT
);

-- évente új táblázat készül az ajánlatoknak
CREATE TABLE IF NOT EXISTS "Ajánlat2019" (
    "szám" TEXT PRIMARY KEY,
    "ajánlatkérés" INTEGER NOT NULL REFERENCES "Ajánlatkérés"("rowid") ON DELETE RESTRICT ON UPDATE RESTRICT,
    "leadva" DATE,
    "érvényes" DATE,
    "ajánlati ár" INTEGER DEFAULT 0,
    "esély" INTEGER DEFAULT 5, -- <100%: esély, 100%: nyert
    "megjegyzés" TEXT
);
