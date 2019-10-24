-- Syntax: SQLite

PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS projekt (
    azonosito INTEGER PRIMARY KEY,
    megnevezes TEXT NOT NULL,
    megjegyzes TEXT DEFAULT ''
);


CREATE TABLE IF NOT EXISTS munkaresz (
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
