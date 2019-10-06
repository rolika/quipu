-- Syntax: SQLite3

CREATE TABLE IF NOT EXISTS "Szervezet" (
    "rövid név" TEXT NOT NULL,
    "teljes név" TEXT NOT NULL,
    "megjegyzés" TEXT
);

CREATE TABLE IF NOT EXISTS "Telefon" (
    "szervezet" INTEGER NOT NULL REFERENCES "Szervezet"("rowid"),
    "telefonszám" TEXT NOT NULL,
    "megjegyzés" TEXT
);

CREATE TABLE IF NOT EXISTS "Email" (
    "szervezet" INTEGER NOT NULL REFERENCES "Szervezet"("rowid"),
    "email-cím" TEXT NOT NULL,
    "megjegyzés" TEXT
);

CREATE TABLE IF NOT EXISTS "Cím" (
    "szervezet" INTEGER NOT NULL REFERENCES "Szervezet"("rowid"),
    "ország" TEXT NOT NULL DEFAULT 'Magyarország',
    "irányítószám" TEXT,
    "helység" TEXT NOT NULL,
    "utca" TEXT, -- házszám is
    "megjegyzés" TEXT
);
