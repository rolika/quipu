-- Syntax: SQLite

CREATE TABLE IF NOT EXISTS "Munka" (
    "megnevezés" TEXT NOT NULL,
    "jelleg" TEXT NOT NULL DEFAULT 'új',
    "megjegyzés" TEXT,
    CONSTRAINT ELL_MNK_JLG CHECK("jelleg" in ('új', 'felújítás', 'bővítés', 'átalakítás', 'bérbeadás', 'eladás'))
);


CREATE TABLE IF NOT EXISTS "Cím" (
    "munka" INTEGER NOT NULL REFERENCES "Munka"("rowid"),
    "ország" TEXT NOT NULL DEFAULT 'Magyarország',
    "irányítószám" TEXT,
    "helység" TEXT NOT NULL,
    "utca" TEXT, -- házszám is
    "hrsz" TEXT,
    "megjegyzés" TEXT
);

CREATE TABLE IF NOT EXISTS "Munkarész" (
    "munka" INTEGER NOT NULL REFERENCES "Munka"("rowid"),
    "megnevezés" TEXT NOT NULL DEFAULT 'hőszigetelés',
    "mennyiség" REAL,
    "egység" TEXT DEFAULT 'm3',
    "anyag" TEXT DEFAULT 'zc',
    "megjegyzés" TEXT,
    CONSTRAINT ELL_MNK_EGS CHECK("egység" in ('m2', 'm3', 'db', 'kg', "szett"))
    CONSTRAINT ELL_MNK_ANG CHECK("anyag" in ('zc', 'nyc', 'fa', 'komponens', 'alkatrész', 'gép'))
);
