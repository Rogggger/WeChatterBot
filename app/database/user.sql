CREATE TABLE user (
  id       INTEGER      NOT NULL AUTO_INCREMENT,
  name     VARCHAR(50)  NOT NULL,
  password VARCHAR(200) NOT NULL,
  salt     VARCHAR(50),
  PRIMARY KEY (id)
)
