-- Syntax: SQLite3

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Személy (
    azonosító INTEGER PRIMARY KEY,
    előtag TEXT DEFAULT '',
    vezetéknév TEXT NOT NULL,
    keresztnév TEXT NOT NULL,
    nem TEXT NOT NULL,
    megjegyzés TEXT DEFAULT '',
    CONSTRAINT ELL_SZEM_NEM CHECK(nem in ('férfi', 'nő'))
);

CREATE TABLE IF NOT EXISTS Telefon (
    személy INTEGER NOT NULL,
    telefonszám TEXT NOT NULL,
    megjegyzés TEXT DEFAULT 'elsődleges',
    FOREIGN KEY(személy) REFERENCES Személy(azonosító) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Email (
    személy INTEGER NOT NULL,
    emailcím TEXT NOT NULL,
    megjegyzés TEXT DEFAULT 'elsődleges',
    FOREIGN KEY(személy) REFERENCES Személy(azonosító) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Cím (
    személy INTEGER NOT NULL,
    ország TEXT NOT NULL DEFAULT 'H',
    irányítószám TEXT DEFAULT '',
    helység TEXT NOT NULL,
    utca TEXT DEFAULT '', -- házszám is
    megjegyzés TEXT DEFAULT 'elsődleges',
    FOREIGN KEY(személy) REFERENCES Személy(azonosító) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Megszólítás (
    nem TEXT,
    megszólítás TEXT
);
INSERT INTO Megszólítás VALUES ("nő", "Hölgyem");
INSERT INTO Megszólítás VALUES ("férfi", "Uram");

CREATE VIEW IF NOT EXISTS Név(személy, név) AS
    SELECT azonosító, ltrim(printf('%s %s %s', előtag, vezetéknév, keresztnév)) FROM Személy;

CREATE VIEW IF NOT EXISTS TeljesCím(személy, cím) AS
    SELECT személy, printf('%s-%s %s, %s', ország, irányítószám, helység, utca) FROM Cím;

CREATE VIEW IF NOT EXISTS Elérhetőség(személy, elérhetőség) AS
    SELECT Név.személy, printf('%s: %s, %s', név, telefonszám, emailcím) FROM Név, Telefon, Email
        WHERE Név.személy=Telefon.személy
            AND Név.személy=Email.személy
            AND Telefon.megjegyzés='elsődleges'
            AND Email.megjegyzés='elsődleges';

CREATE VIEW IF NOT EXISTS Köszöntés(személy, köszöntés) AS
    SELECT Személy.azonosító, printf('Tisztelt %s!', megszólítás) FROM Személy, Megszólítás
        WHERE Személy.nem=Megszólítás.nem;
