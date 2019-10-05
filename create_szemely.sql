-- táblatörlés: tesztelés, debugolás
DROP TABLE IF EXISTS "Személy";
DROP TABLE IF EXISTS "Nem";
DROP TABLE IF EXISTS "Köszöntés";
DROP TABLE IF EXISTS "Megszólítás";
DROP TABLE IF EXISTS "Telefon";
DROP TABLE IF EXISTS "Email";
DROP TABLE IF EXISTS "Cím";
DROP TABLE IF EXISTS "NÜJ";
DROP TABLE IF EXISTS "FMV";
DROP TABLE IF EXISTS "Munkavállaló";

-- gdpr-érzékeny
-- ha törlődik a személy, törlődik a hozzátartozó összes adat rá hivatkozó táblákban
CREATE TABLE IF NOT EXISTS "Személy" (
    "előtag" TEXT(10),
    "vezetéknév" TEXT(30),
    "keresztnév" TEXT(30),
    "tegező" BOOLEAN DEFAULT NULL,
    "nem" INTEGER REFERENCES "Nem"("rowid"),
    "megjegyzés" TEXT(50),
    "törlendő" DATE -- ha eléri a dátumot, törli a személyt
);

CREATE TABLE IF NOT EXISTS "Nem" (
    "nem" TEXT(5)
);
INSERT INTO "Nem"("nem") VALUES ('férfi');
INSERT INTO "Nem"("nem") VALUES ('nő');

CREATE TABLE IF NOT EXISTS "Köszöntés" (
    "köszöntés" TEXT(8)
);
INSERT INTO "Köszöntés"("köszöntés") VALUES ('Kedves');
INSERT INTO "Köszöntés"("köszöntés") VALUES ('Tisztelt');

CREATE TABLE IF NOT EXISTS "Megszólítás" (
    "megszólítás" TEXT(7)
);
INSERT INTO "Megszólítás"("megszólítás") VALUES ('Hölgyem');
INSERT INTO "Megszólítás"("megszólítás") VALUES ('Uram');

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Telefon" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "telefonszám" TEXT(20),
    "megjegyzés" TEXT(50)
);
-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Email" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "email-cím" TEXT(50),
    "megjegyzés" TEXT(50)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "Cím" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "ország" TEXT(50) DEFAULT 'Magyarország',
    "irányítószám" TEXT(10),
    "helység" TEXT(50),
    "utca, házszám" TEXT(50),
    "megjegyzés" TEXT(50)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "NÜJ" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "nüj" TEXT(20)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "FMV" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "fmv-szám" TEXT(20)
);

-- gdpr-érzékeny
-- személyadatok munkaviszonyhoz
CREATE TABLE IF NOT EXISTS "Munkavállaló" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "születési név" TEXT(60),
    "születési hely" TEXT(50),
    "születési idő" DATE,
    "édesanyja neve" TEXT(60),
    "taj-szám" TEXT(20),
    "adóazonosító jel" TEXT(20)
);
