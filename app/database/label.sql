CREATE TABLE label (
  id          INTEGER     NOT NULL,
  name        VARCHAR(50) NOT NULL,
  color       INTEGER     NOT NULL DEFAULT 0,
  user_id     INTEGER     NOT NULL,
  last_edited TIMESTAMP   NOT NULL DEFAULT '1980-01-01 00:00:00',
  deleted     BOOL        NOT NULL,
  PRIMARY KEY (id, user_id),
  FOREIGN KEY (user_id) REFERENCES user (id),
  CHECK (deleted IN (0, 1))
)
