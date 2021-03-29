-- SQLite3 db
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL, -- email can also be used to identify a user
  password TEXT NOT NULL
);

-- Initialize flaskr in db with example flaskr
INSERT INTO user VALUES (0, "hassan", "hassan149367@gmail.com", "password");
