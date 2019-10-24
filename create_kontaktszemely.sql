-- Syntax: SQLite3

PRAGMA foreign_key = ON;

ATTACH DATABASE "szemely.db" AS "szemely";
ATTACH DATABASE "szervezet.db" AS "szervezet";


CREATE TABLE IF NOT EXISTS kontaktszemely (
    azonosito INTEGER PRIMARY KEY,
    szemely INTEGER NOT NULL REFERENCES szemely(szemely),
    szervezet INTEGER REFERENCES szervezet(szervezet),
    megjegyzes TEXT DEFAULT ''
);
