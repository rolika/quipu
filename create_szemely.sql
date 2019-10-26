-- Syntax: SQLite3

PRAGMA foreign_keys = ON;

ATTACH DATABASE "szervezet.db" AS szervezet;


CREATE TABLE IF NOT EXISTS megszolitas (
    nem TEXT PRIMARY KEY,
    megszolitas TEXT
);
INSERT INTO megszolitas VALUES ("nő", "Hölgyem");
INSERT INTO megszolitas VALUES ("férfi", "Uram");


CREATE TABLE IF NOT EXISTS szemely (
    azonosito INTEGER PRIMARY KEY,
    elotag TEXT DEFAULT '',
    vezeteknev TEXT NOT NULL,
    keresztnev TEXT NOT NULL,
    nem TEXT NOT NULL REFERENCES megszolitas,
    megjegyzes TEXT DEFAULT ''
);


CREATE TABLE IF NOT EXISTS telefon (
    szemely INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE,
    telefonszam TEXT NOT NULL,
    megjegyzes TEXT DEFAULT 'elsődleges'
);


CREATE TABLE IF NOT EXISTS email (
    szemely INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE,
    emailcim TEXT NOT NULL,
    megjegyzes TEXT DEFAULT 'elsődleges'
);


CREATE TABLE IF NOT EXISTS cim (
    szemely INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE,
    orszag TEXT NOT NULL DEFAULT 'H',
    iranyitoszam TEXT DEFAULT '',
    helyseg TEXT NOT NULL,
    utca TEXT DEFAULT '', -- házszám is
    megjegyzes TEXT DEFAULT 'elsődleges'
);


CREATE TABLE IF NOT EXISTS kontakt (
    azonosito INTEGER PRIMARY KEY,
    szemely INTEGER NOT NULL REFERENCES szemely,
    szervezet INTEGER REFERENCES szervezet(szervezet),
    megjegyzes TEXT DEFAULT ''
);


CREATE VIEW IF NOT EXISTS nev(szemely, nev) AS
    SELECT azonosito, ltrim(printf('%s %s %s', elotag, vezeteknev, keresztnev))
        FROM szemely;


CREATE VIEW IF NOT EXISTS teljescim(szemely, cim) AS
    SELECT szemely, printf('%s-%s %s, %s', orszag, iranyitoszam, helyseg, utca)
        FROM cim;


CREATE VIEW IF NOT EXISTS elerhetoseg(szemely, elerhetoseg) AS
    SELECT nev.szemely, printf('%s: %s, %s', nev, telefonszam, emailcim)
        FROM nev, telefon, email
            WHERE nev.szemely=telefon.szemely
                AND nev.szemely=email.szemely
                AND telefon.megjegyzes='elsődleges'
                AND email.megjegyzes='elsődleges';


CREATE VIEW IF NOT EXISTS koszontes(szemely, koszontes) AS
    SELECT szemely.azonosito, printf('Tisztelt %s!', megszolitas)
        FROM szemely, megszolitas
            WHERE szemely.nem=megszolitas.nem;


-- automatikusan add hozzá a kontaktszemélyhez is
CREATE TRIGGER IF NOT EXISTS kntkt AFTER INSERT ON szemely
    BEGIN
        INSERT INTO kontakt(szemely) VALUES(last_insert_rowid());
    END;