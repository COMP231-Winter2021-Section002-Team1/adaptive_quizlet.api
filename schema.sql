
-- SQLite3 db
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS quiz;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL, -- email can also be used to identify a user
  password TEXT NOT NULL
);

CREATE TABLE quiz (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  author_id INTEGER,
  quiz_type TEXT,
  visibility BOOLEAN NOT NULL,
  FOREIGN KEY(author_id) REFERENCES user(id)
);

-- Initialize data in db with example data
INSERT INTO user VALUES (0, "hassan", "hassan149367@gmail.com", "password");
INSERT INTO quiz VALUES (0, "Hassan's Trivia Quiz", 0, "Normal", TRUE);