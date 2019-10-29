-- Syntax: SQLite3

PRAGMA foreign_keys = ON;

ATTACH DATABASE "szemely.db" AS szemely;
ATTACH DATABASE "munka.db" AS munka;


CREATE TABLE IF NOT EXISTS ajanlatkeres (
    azonosito INTEGER PRIMARY KEY,
    ajanlatkero INTEGER NOT NULL, -- szemely.kontakt
    munkaresz INTEGER NOT NULL, -- munka.munkaresz
    erkezett DATE DEFAULT (date('now')),
    hatarido DATE DEFAULT (date('now', '+7 day')),
    temafelelos INTEGER, -- szemely.kontakt
    megjegyzes TEXT
);


CREATE TABLE IF NOT EXISTS ajanlat (
    ev INTEGER DEFAULT 19, --a biztonság kedvéért, ha a trigger mégsem fut le
    szam INTEGER DEFAULT 0, --első érték a triggerben lévő max()-hoz
    ajanlatkeres INTEGER NOT NULL REFERENCES ajanlatkeres,
    leadva DATE DEFAULT (date('now')),
    ervenyes DATE DEFAULT (date('now', '+30 day')),
    ar INTEGER NOT NULL,
    esely INTEGER DEFAULT 5, -- <100%: esély, 100%: nyert
    megjegyzes TEXT,
    PRIMARY KEY(ev, szam) ON CONFLICT REPLACE
);


/*
Következő projektszám előállítása.
Formátum: éé/szám, pl. 19/3
*/
CREATE TRIGGER PRSZAM AFTER INSERT ON ajanlat
    BEGIN
        UPDATE ajanlat SET ev=substr(date('now'),3,2) WHERE rowid=last_insert_rowid();
        UPDATE ajanlat SET szam=(
            SELECT max(szam)+1 FROM ajanlat WHERE ev=substr(date('now'),3,2)
        /* Ha az első update szilveszter éjfél előtt fut le, a második pedig éjfél
        után, akkor NULL lesz a szám (+1-gyel együtt is). Vállalható kockázat :-) */
        ) WHERE rowid=last_insert_rowid();
    END;
