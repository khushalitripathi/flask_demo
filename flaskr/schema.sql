DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  address TEXT NOT NULL,
  marital_status TEXT NOT NULL,
  salary INTEGER NOT NULL
);