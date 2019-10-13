-- Syntax: SQLite3

PRAGMA foreign_keys = ON;

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Személy" (
    "előtag" TEXT DEFAULT '',
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
    "megjegyzés" TEXT DEFAULT 'elsődleges'
);
-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Email" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "email-cím" TEXT NOT NULL,
    "megjegyzés" TEXT DEFAULT 'elsődleges'
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Cím" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "ország" TEXT NOT NULL DEFAULT 'Magyarország',
    "irányítószám" TEXT,
    "helység" TEXT NOT NULL,
    "utca" TEXT, -- házszám is
    "megjegyzés" TEXT DEFAULT 'elsődleges'
);

CREATE TABLE IF NOT EXISTS "Megszólítás" (
    "nem" TEXT PRIMARY KEY REFERENCES "Személy"("nem"),
    "megszólítás" TEXT
);
INSERT INTO "Megszólítás" VALUES ("nő", "Hölgyem");
INSERT INTO "Megszólítás" VALUES ("férfi", "Uram");

CREATE VIEW IF NOT EXISTS "Név"("személy", "név") AS
    SELECT "rowid", ltrim(printf('%s %s %s', "előtag", "vezetéknév", "keresztnév")) FROM "Személy";

CREATE VIEW IF NOT EXISTS "Teljes cím"("személy", "cím") AS
    SELECT "személy", printf('%s-%s, %s (%s)', "irányítószám", "helység", "utca", "ország") FROM "Cím";

CREATE VIEW IF NOT EXISTS "Elérhetőség"("személy", "elérhetőség") AS
    SELECT "személy", printf('%s: %s, %s', "név", "telefonszám", "email-cím") FROM "Név", "Telefon", "Email"
        WHERE "személy"="Telefon"."személy"
            AND "személy"="Email"."személy"
            AND "Telefon"."megjegyzés"='elsődleges'
            AND "Email"."megjegyzés"='elsődleges';

CREATE VIEW IF NOT EXISTS "Köszöntés"("személy", "köszöntés") AS
    SELECT "Személy"."rowid", printf('Tisztelt %s!', "megszólítás") FROM "Személy", "Megszólítás"
        WHERE "Személy"."nem"="Megszólítás"."nem";
