CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    hpsw text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    post_id integer PRIMARY KEY AUTOINCREMENT,
    user_id integer NOT NULL,
    title text NOT NULL,
    text text,
    time integer NOT NULL
)