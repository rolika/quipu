-- Syntax: SQLite3

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Személy" (
    "előtag" TEXT,
    "vezetéknév" TEXT NOT NULL,
    "keresztnév" TEXT NOT NULL,
    "nem" TEXT,
    "érvényes" DATE, -- ha eléri a dátumot, törli a személyt és a hozzá kapcsolódó összes adatot
    "megjegyzés" TEXT,
    CONSTRAINT ELL_SZEM_NEM CHECK("nem" in ('férfi', 'nő'))
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Telefon" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "telefonszám" TEXT NOT NULL,
    "megjegyzés" TEXT
);
-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Email" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "email-cím" TEXT NOT NULL,
    "megjegyzés" TEXT
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Cím" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "ország" TEXT NOT NULL DEFAULT 'Magyarország',
    "irányítószám" TEXT,
    "helység" TEXT NOT NULL,
    "utca" TEXT, -- házszám is
    "megjegyzés" TEXT
);
