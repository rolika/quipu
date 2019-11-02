/*
Néhány fontosabb SELECT
*/


-- kontaktszemely.db
SELECT printf('%s (%d): %s (%d)', szervezet.rovidnev, szervezet.azonosito, nev.nev, nev.szemely)
    FROM kontaktszemely, szervezet.szervezet, szemely.nev
        WHERE kontaktszemely.szemely=nev.szemely
            AND kontaktszemely.szervezet=szervezet.azonosito;