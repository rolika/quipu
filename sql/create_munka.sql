-- Syntax: SQLite

PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS projekt (
    azonosito INTEGER PRIMARY KEY,
    megnevezes TEXT NOT NULL,
    rovidnev TEXT DEFAULT '',
    megjegyzes TEXT DEFAULT ''
);


CREATE TABLE IF NOT EXISTS munkaresz (
    azonosito INTEGER PRIMARY KEY,
    projekt INTEGER NOT NULL REFERENCES projekt,
    megnevezes TEXT NOT NULL DEFAULT 'szigetelés',
    megjegyzes TEXT DEFAULT ''
);


CREATE TABLE IF NOT EXISTS cim (
    projekt INTEGER NOT NULL REFERENCES projekt,
    orszag TEXT NOT NULL DEFAULT 'H',
    megye TEXT NOT NULL DEFAULT '',
    iranyitoszam TEXT DEFAULT '',
    helyseg TEXT NOT NULL,
    utca TEXT DEFAULT '', -- házszám is
    hrsz TEXT DEFAULT '',
    megjegyzes TEXT DEFAULT ''
);


CREATE TABLE IF NOT EXISTS jelleg (
    projekt INTEGER NOT NULL REFERENCES projekt,
    megnevezes TEXT NOT NULL DEFAULT 'új',
    megjegyzes TEXT DEFAULT '',
    CONSTRAINT ELL_JLG CHECK(megnevezes in ('új', 'felújítás', 'bővítés', 'átalakítás', 'bérbeadás', 'értékesítés'))
);


CREATE VIEW nev(projekt, nev) AS
    SELECT projekt.azonosito, printf('%s, %s, %s', projekt.megnevezes, helyseg, lower(munkaresz.megnevezes))
        FROM projekt, cim, munkaresz
            WHERE projekt.azonosito=cim.projekt
                AND projekt.azonosito=munkaresz.projekt;
