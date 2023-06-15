DROP TABLE IF EXISTS awaitrecipes;

CREATE TABLE awaitrecipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rname TEXT NOT NULL,
    rcategory TEXT NOT NULL,
    rimage  TEXT NOT NULL,
    image1 TEXT,
    image2 TEXT,
    image3 TEXT,
    rdescription TEXT NOT NULL,
    ringredients TEXT NOT NULL,
    rprocedure TEXT NOT NULL
);

