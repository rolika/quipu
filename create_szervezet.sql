-- Syntax: SQLite3

PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS szervezet (
    azonosito INTEGER PRIMARY KEY,
    rovidnev TEXT NOT NULL,
    teljesnev TEXT NOT NULL,
    megjegyzes TEXT
);


CREATE TABLE IF NOT EXISTS telefon (
    szervezet INTEGER NOT NULL REFERENCES szervezet,
    telefonszam TEXT NOT NULL,
    megjegyzes TEXT DEFAULT 'elsődleges'
);


CREATE TABLE IF NOT EXISTS email (
    szervezet INTEGER NOT NULL REFERENCES szervezet,
    emailcim TEXT NOT NULL,
    megjegyzes TEXT DEFAULT 'elsődleges'
);


CREATE TABLE IF NOT EXISTS cim (
    szervezet INTEGER NOT NULL REFERENCES szervezet ON DELETE CASCADE,
    orszag TEXT NOT NULL DEFAULT 'H',
    iranyitoszam TEXT DEFAULT '',
    helyseg TEXT NOT NULL,
    utca TEXT DEFAULT '', -- házszám is
    megjegyzes TEXT DEFAULT 'székhely'
);


CREATE VIEW IF NOT EXISTS teljescim(szervezet, cim) AS
    SELECT szervezet, printf('%s-%s %s, %s', orszag, iranyitoszam, helyseg, utca)
        FROM cim;
