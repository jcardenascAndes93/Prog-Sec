INSERT INTO user (username, password)
VALUES
  ('test', 'test'),
  ('other', 'other');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test\nbody', 1, '2018-01-01 00:00:00');
