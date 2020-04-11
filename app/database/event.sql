CREATE TABLE event (
  id          INTEGER     NOT NULL,
  task        VARCHAR(50) NOT NULL,
  note        VARCHAR(500),
  label_id    INTEGER,
  user_id     INTEGER     NOT NULL,
  deadline    TIMESTAMP   NOT NULL DEFAULT '1980-01-01 00:00:00',
  reminders   VARCHAR(50),
  last_edited TIMESTAMP   NOT NULL DEFAULT '1980-01-01 00:00:00',
  deleted     BOOL        NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (label_id) REFERENCES label (id),
  FOREIGN KEY (user_id) REFERENCES user (id),
  CHECK (deleted IN (0, 1))
)
