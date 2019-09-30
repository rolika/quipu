DROP TABLE IF EXISTS "Megye";
DROP TABLE IF EXISTS "Személy";
DROP TABLE IF EXISTS "SzemélyElérhetőség";
DROP TABLE IF EXISTS "SzemélyCím";
DROP TABLE IF EXISTS "SzemélyAdat";
DROP TABLE IF EXISTS "SzemélyFMV";

DROP TABLE IF EXISTS "Cég";
DROP TABLE IF EXISTS "CégElérhetőség";
DROP TABLE IF EXISTS "CégCím";
DROP TABLE IF EXISTS "CégAdat";

DROP TABLE IF EXISTS "SzemélyBankiKapcsolat";
DROP TABLE IF EXISTS "CégBankiKapcsolat";
DROP TABLE IF EXISTS "Kontaktszemély";
DROP TABLE IF EXISTS "Építkezés";

DROP TABLE IF EXISTS "Munkarész";
DROP TABLE IF EXISTS "ÉpítkezésCím";
DROP TABLE IF EXISTS "Árajánlat";

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "Megye" (
    "név" TEXT(25) NOT NULL
);

INSERT INTO "Megye"("név") VALUES('Bács-Kiskun');
INSERT INTO "Megye"("név") VALUES('Baranya');
INSERT INTO "Megye"("név") VALUES('Békés');
INSERT INTO "Megye"("név") VALUES('Borsod-Abaúj-Zemplén');
INSERT INTO "Megye"("név") VALUES('Budapest');
INSERT INTO "Megye"("név") VALUES('Csongrád');
INSERT INTO "Megye"("név") VALUES('Fejér');
INSERT INTO "Megye"("név") VALUES('Győr-Moson-Sopron');
INSERT INTO "Megye"("név") VALUES('Hajdú-Bihar');
INSERT INTO "Megye"("név") VALUES('Heves');
INSERT INTO "Megye"("név") VALUES('Jász-Nagykun-Szolnok');
INSERT INTO "Megye"("név") VALUES('Komárom-Esztergom');
INSERT INTO "Megye"("név") VALUES('Nógrád');
INSERT INTO "Megye"("név") VALUES('Pest');
INSERT INTO "Megye"("név") VALUES('Somogy');
INSERT INTO "Megye"("név") VALUES('Szabolcs-Szatmár-Bereg');
INSERT INTO "Megye"("név") VALUES('Tolna');
INSERT INTO "Megye"("név") VALUES('Vas');
INSERT INTO "Megye"("név") VALUES('Veszprém');
INSERT INTO "Megye"("név") VALUES('Zala');

-- gdpr-érzékeny
-- ha törlődik a személy, törlődik a hozzátartozó összes adat rá hivatkozó táblákban
CREATE TABLE IF NOT EXISTS "Személy" (
    "előtag" TEXT(10),
    "vezetéknév" TEXT(30),
    "keresztnév" TEXT(30),
    "nem" TEXT(5),
    "megjegyzés" TEXT(50),
    "törlendő" DATE, -- ha eléri a dátumot, törli a személyt
    CONSTRAINT ELL_SZEM_NEM CHECK("nem" in ('férfi', 'nő'))
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "SzemélyElérhetőség" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "telefonszám" TEXT(20),
    "email-cím" TEXT(50),
    "megjegyzés" TEXT(50)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "SzemélyCím" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "ország" TEXT(50) DEFAULT 'Magyarország',
    "megye" INTEGER REFERENCES "Megye"("rowid"),
    "irányítószám" TEXT(10),
    "helység" TEXT(50),
    "utca, házszám" TEXT(50),
    "megjegyzés" TEXT(50)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "SzemélyAdat" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "születési név" TEXT(60),
    "születési hely" TEXT(50),
    "születési idő" DATE,
    "édesanyja neve" TEXT(60),
    "taj-szám" TEXT(20),
    "adóazonosító jel" TEXT(20),
    "nüj" TEXT(20)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "SzemélyFMV" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "fmv-szám" TEXT(20)
);

CREATE TABLE IF NOT EXISTS "Cég" (
    "rövid név" TEXT(50) NOT NULL,
    "teljes név" TEXT(100),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "CégElérhetőség" (
    "cég" INTEGER NOT NULL REFERENCES "Cég"("rowid") ON DELETE RESTRICT ON UPDATE CASCADE,
    "telefonszám" TEXT(20),
    "email-cím" TEXT(50),
    "web" TEXT(50),
    "telefax" TEXT(20),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "CégCím" (
    "cég" INTEGER NOT NULL REFERENCES "Cég"("rowid") ON DELETE RESTRICT ON UPDATE CASCADE,
    "ország" TEXT(50) DEFAULT 'Magyarország',
    "megye" INTEGER REFERENCES "Megye"("rowid"),
    "irányítószám" TEXT(10),
    "helység" TEXT(50),
    "utca, házszám" TEXT(50),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "CégAdat" (
    "cég" INTEGER NOT NULL REFERENCES "Cég"("rowid") ON DELETE RESTRICT ON UPDATE CASCADE,
    "adószám" TEXT(20),
    "cégjegyzék-szám" TEXT(20),
    "kamarai-szám" TEXT(20),
    "uniós adószám" TEXT(20),
    "megjegyzés" TEXT(50)
);

-- gdpr-érzékeny
CREATE TABLE IF NOT EXISTS "SzemélyBankiKapcsolat" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "bank" INTEGER REFERENCES "Cég"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "számlaszám" TEXT(50),
    "IBAN" TEXT(50),
    "SWIFT" TEXT(20),
    "pénznem" TEXT(5),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "CégBankiKapcsolat" (
    "cég" INTEGER NOT NULL REFERENCES "Cég"("rowid") ON DELETE RESTRICT ON UPDATE CASCADE,
    "bank" INTEGER REFERENCES "Cég"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "számlaszám" TEXT(50),
    "IBAN" TEXT(50),
    "SWIFT" TEXT(20),
    "pénznem" TEXT(5),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "KontaktSzemély" (
    "személy" INTEGER NOT NULL REFERENCES "Személy"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "cég" INTEGER REFERENCES "Cég"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "Éptkezés" (
    "megnevezés" TEXT(100) NOT NULL,
    "jelleg" TEXT(50),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "Munkarész" (
    "építkezés" INTEGER NOT NULL REFERENCES "Építkezés"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "munkarész" TEXT(50) NOT NULL  DEFAULT 'szigetelés',
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "ÉpítkezésCím" (
    "építkezés" INTEGER NOT NULL REFERENCES "Építkezés"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "ország" TEXT(50) DEFAULT 'Magyarország',
    "megye" INTEGER REFERENCES "Megye"("rowid"),
    "irányítószám" TEXT(10),
    "helység" TEXT(50),
    "utca, házszám" TEXT(50),
    "megjegyzés" TEXT(50)
);

CREATE TABLE IF NOT EXISTS "Árajánlat" (
    "szám" TEXT(10) UNIQUE,
    "munkarész" INTEGER NOT NULL REFERENCES "Munkarész"("rowid") ON DELETE CASCADE ON UPDATE CASCADE,
    "kontaktszemély" INTEGER REFERENCES "Kontaktszemély"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "témafelelős" INTEGER REFERENCES "Kontaktszemély"("rowid") ON DELETE SET NULL ON UPDATE CASCADE,
    "érkezett" DATE DEFAULT (date('now')),
    "leadási határidő" DATE DEFAULT (date('now', '+5 day')),
    "leadva" DATE,
    "érvényes" DATE,
    "ajánlati ár" INTEGER DEFAULT 0,
    /* 
       %os esély magyarázat:
       <100%: esély, 100%: nyert, 101%: aktuális, 102%: kész, 103%: végszámlázva, 104%: fizetve
       100% és fölötte már nincs kijelezve
    */
    "esély" INTEGER DEFAULT 5,
    "megjegyzés" TEXT(50)
);
