-- Syntax: SQLite

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "Munka" (
    "megnevezés" TEXT NOT NULL,
    "jelleg" TEXT NOT NULL DEFAULT 'új',
    "megjegyzés" TEXT,
    CONSTRAINT ELL_MNK_JLG CHECK("jelleg" in ('új', 'felújítás', 'bővítés', 'átalakítás', 'bérbeadás', 'eladás'))
);


CREATE TABLE IF NOT EXISTS "Cím" (
    "munka" INTEGER NOT NULL REFERENCES "Munka"("rowid"),
    "ország" TEXT NOT NULL DEFAULT 'Magyarország',
    "megye" TEXT,
    "irányítószám" TEXT,
    "helység" TEXT NOT NULL,
    "utca" TEXT, -- házszám is
    "hrsz" TEXT,
    "megjegyzés" TEXT
);

CREATE TABLE IF NOT EXISTS "Munkarész" (
    "munka" INTEGER NOT NULL REFERENCES "Munka"("rowid"),
    "megnevezés" TEXT NOT NULL DEFAULT 'hőszigetelés'
    "megjegyzés" TEXT
);
