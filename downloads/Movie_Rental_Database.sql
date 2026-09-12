/* Movie Rental Database - academic final project by Jonathan Capalbo.
   Portfolio copy: customer names and contact details replaced with fictional examples.
   Movie-to-actor assignments are sample relationships, not factual casting credits.
   Schema, SQL logic, and record counts are unchanged from the class submission.
   Saved as UTF-8 without a BOM for SQL*Plus compatibility.
   Run as a script in a fresh Oracle schema; existing objects will cause errors.
   The original uses English month abbreviations; use an English date language.
   Known gaps: return dates may precede rental dates, and a copy may have more
   than one open rental. See the portfolio validation summary before reuse.
*/

/* 1. Create Tables */
CREATE TABLE customers (
  customer_id  NUMBER(10)    NOT NULL,
  last_name    VARCHAR2(50)  NOT NULL,
  first_name   VARCHAR2(50)  NOT NULL,
  home_phone   VARCHAR2(20)  NOT NULL,
  address      VARCHAR2(100) NOT NULL,
  city         VARCHAR2(50)  NOT NULL,
  state        CHAR(2)       NOT NULL,
  email        VARCHAR2(100),
  cell_phone   VARCHAR2(20)
);

CREATE TABLE movies (
  title_id      NUMBER(10)    NOT NULL,
  title         VARCHAR2(100) NOT NULL,
  description   VARCHAR2(500) NOT NULL,
  rating        VARCHAR2(5),
  category      VARCHAR2(20)  NOT NULL,
  release_date  DATE          NOT NULL
);

CREATE TABLE media (
  media_id  NUMBER(10)   NOT NULL,
  title_id  NUMBER(10)   NOT NULL,
  format    VARCHAR2(20) NOT NULL
);

CREATE TABLE actors (
  actor_id    NUMBER(10)    NOT NULL,
  stage_name  VARCHAR2(60)  NOT NULL,
  first_name  VARCHAR2(50)  NOT NULL,
  last_name   VARCHAR2(50)  NOT NULL,
  birth_date  DATE          NOT NULL
);

CREATE TABLE star_billings (
  title_id  NUMBER(10) NOT NULL,
  actor_id  NUMBER(10) NOT NULL,
  "comment" VARCHAR2(200)
);

CREATE TABLE rental_history (
  media_id     NUMBER(10) NOT NULL,
  customer_id  NUMBER(10) NOT NULL,
  rental_date  DATE DEFAULT SYSDATE NOT NULL,
  return_date  DATE
);

DESC customers;
DESC movies;
DESC media;
DESC actors;
DESC star_billings;
DESC rental_history;

/* 2. Integrity Constraints */
ALTER TABLE customers ADD CONSTRAINT customers_pk PRIMARY KEY (customer_id);
ALTER TABLE movies ADD CONSTRAINT movies_pk PRIMARY KEY (title_id);
ALTER TABLE media ADD CONSTRAINT media_pk PRIMARY KEY (media_id);
ALTER TABLE actors ADD CONSTRAINT actors_pk PRIMARY KEY (actor_id);
ALTER TABLE star_billings ADD CONSTRAINT star_billings_pk PRIMARY KEY (title_id, actor_id);
ALTER TABLE rental_history ADD CONSTRAINT rental_history_pk PRIMARY KEY (media_id, rental_date);

ALTER TABLE media ADD CONSTRAINT media_movies_fk FOREIGN KEY (title_id) REFERENCES movies(title_id);
ALTER TABLE star_billings ADD CONSTRAINT starb_movies_fk FOREIGN KEY (title_id) REFERENCES movies(title_id);
ALTER TABLE star_billings ADD CONSTRAINT starb_actors_fk FOREIGN KEY (actor_id) REFERENCES actors(actor_id);
ALTER TABLE rental_history ADD CONSTRAINT rental_media_fk FOREIGN KEY (media_id) REFERENCES media(media_id);
ALTER TABLE rental_history ADD CONSTRAINT rental_customers_fk FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE movies ADD CONSTRAINT movies_rating_ck CHECK (rating IN ('G','PG','R','PG13'));
ALTER TABLE movies ADD CONSTRAINT movies_category_ck CHECK (category IN ('DRAMA','COMEDY','ACTION','CHILD','SCIFI','DOCUMENTARY'));

SELECT table_name, constraint_name, constraint_type, status
FROM user_constraints
WHERE table_name IN ('CUSTOMERS','MOVIES','MEDIA','ACTORS','STAR_BILLINGS','RENTAL_HISTORY')
ORDER BY table_name, constraint_type, constraint_name;

SELECT table_name, constraint_name, column_name, position
FROM user_cons_columns
WHERE table_name IN ('CUSTOMERS','MOVIES','MEDIA','ACTORS','STAR_BILLINGS','RENTAL_HISTORY')
ORDER BY table_name, constraint_name, position;

/* 3. Create View */
CREATE OR REPLACE VIEW title_unavail AS
SELECT m.title, me.media_id
FROM movies m
JOIN media me ON me.title_id = m.title_id
JOIN rental_history rh ON rh.media_id = me.media_id
WHERE rh.return_date IS NULL
WITH READ ONLY;

/* 4. Create Sequences */
CREATE SEQUENCE customers_seq START WITH 101  INCREMENT BY 1;
CREATE SEQUENCE movies_seq    START WITH 1    INCREMENT BY 1;
CREATE SEQUENCE media_seq     START WITH 92   INCREMENT BY 1;
CREATE SEQUENCE actors_seq    START WITH 1001 INCREMENT BY 1;

SELECT sequence_name, increment_by, last_number
FROM user_sequences
WHERE sequence_name IN ('CUSTOMERS_SEQ','MOVIES_SEQ','MEDIA_SEQ','ACTORS_SEQ')
ORDER BY sequence_name;

/* 5. Add Data */
INSERT INTO customers (customer_id, last_name, first_name, home_phone, address, city, state, email, cell_phone) VALUES (customers_seq.NEXTVAL, 'One', 'Sample', '202-555-0101', '101 Example Lane', 'Exampletown', 'NJ', 'customer1@example.com', '202-555-0111');
INSERT INTO customers (customer_id, last_name, first_name, home_phone, address, city, state, email, cell_phone) VALUES (customers_seq.NEXTVAL, 'Two', 'Sample', '202-555-0102', '102 Example Lane', 'Exampletown', 'NJ', 'customer2@example.com', '202-555-0112');
INSERT INTO customers (customer_id, last_name, first_name, home_phone, address, city, state, email, cell_phone) VALUES (customers_seq.NEXTVAL, 'Three', 'Sample', '202-555-0103', '103 Example Lane', 'Exampletown', 'NJ', 'customer3@example.com', '202-555-0113');
INSERT INTO customers (customer_id, last_name, first_name, home_phone, address, city, state, email, cell_phone) VALUES (customers_seq.NEXTVAL, 'Four', 'Sample', '202-555-0104', '104 Example Lane', 'Exampletown', 'NJ', 'customer4@example.com', '202-555-0114');
INSERT INTO customers (customer_id, last_name, first_name, home_phone, address, city, state, email, cell_phone) VALUES (customers_seq.NEXTVAL, 'Five', 'Sample', '202-555-0105', '105 Example Lane', 'Exampletown', 'NJ', 'customer5@example.com', '202-555-0115');
INSERT INTO customers (customer_id, last_name, first_name, home_phone, address, city, state, email, cell_phone) VALUES (customers_seq.NEXTVAL, 'Six', 'Sample', '202-555-0106', '106 Example Lane', 'Exampletown', 'NJ', 'customer6@example.com', '202-555-0116');

INSERT INTO movies (title_id, title, description, rating, category, release_date) VALUES (movies_seq.NEXTVAL, 'The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son.', 'R', 'DRAMA', TO_DATE('24-MAR-1972','DD-MON-YYYY'));
INSERT INTO movies (title_id, title, description, rating, category, release_date) VALUES (movies_seq.NEXTVAL, 'The Shawshank Redemption', 'Two imprisoned men bond over years, finding redemption through acts of decency and hope.', 'R', 'DRAMA', TO_DATE('14-OCT-1994','DD-MON-YYYY'));
INSERT INTO movies (title_id, title, description, rating, category, release_date) VALUES (movies_seq.NEXTVAL, 'The Dark Knight', 'Batman faces the Joker, a criminal mastermind bent on plunging Gotham into chaos.', 'PG13', 'ACTION', TO_DATE('18-JUL-2008','DD-MON-YYYY'));
INSERT INTO movies (title_id, title, description, rating, category, release_date) VALUES (movies_seq.NEXTVAL, 'Forrest Gump', 'A man with a simple outlook influences several historical events in the 20th century.', 'PG13', 'DRAMA', TO_DATE('06-JUL-1994','DD-MON-YYYY'));
INSERT INTO movies (title_id, title, description, rating, category, release_date) VALUES (movies_seq.NEXTVAL, 'Toy Story', 'A cowboy doll feels threatened when a new spaceman toy becomes the favorite.', 'G', 'CHILD', TO_DATE('22-NOV-1995','DD-MON-YYYY'));
INSERT INTO movies (title_id, title, description, rating, category, release_date) VALUES (movies_seq.NEXTVAL, 'Star Wars: A New Hope', 'A farm boy joins a rebellion to save a princess and defeat an evil empire.', 'PG', 'SCIFI', TO_DATE('25-MAY-1977','DD-MON-YYYY'));

INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 1, 'DVD');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 1, 'VHS');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 2, 'DVD');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 3, 'DVD');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 3, 'VHS');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 4, 'DVD');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 5, 'DVD');
INSERT INTO media (media_id, title_id, format) VALUES (media_seq.NEXTVAL, 6, 'DVD');

INSERT INTO actors (actor_id, stage_name, first_name, last_name, birth_date) VALUES (actors_seq.NEXTVAL, 'Brad Pitt', 'William', 'Pitt', TO_DATE('18-DEC-1963','DD-MON-YYYY'));
INSERT INTO actors (actor_id, stage_name, first_name, last_name, birth_date) VALUES (actors_seq.NEXTVAL, 'Meryl Streep', 'Mary', 'Streep', TO_DATE('22-JUN-1949','DD-MON-YYYY'));
INSERT INTO actors (actor_id, stage_name, first_name, last_name, birth_date) VALUES (actors_seq.NEXTVAL, 'Denzel Washington', 'Denzel', 'Washington', TO_DATE('28-DEC-1954','DD-MON-YYYY'));
INSERT INTO actors (actor_id, stage_name, first_name, last_name, birth_date) VALUES (actors_seq.NEXTVAL, 'Scarlett Johansson', 'Scarlett', 'Johansson', TO_DATE('22-NOV-1984','DD-MON-YYYY'));

INSERT INTO star_billings (title_id, actor_id, "comment") VALUES (2, 1001, 'Romantic Lead');
INSERT INTO star_billings (title_id, actor_id, "comment") VALUES (1, 1002, 'Supporting');
INSERT INTO star_billings (title_id, actor_id, "comment") VALUES (3, 1003, 'Lead');
INSERT INTO star_billings (title_id, actor_id, "comment") VALUES (6, 1004, 'Cameo');

INSERT INTO rental_history (media_id, rental_date, customer_id, return_date) VALUES (92, TO_DATE('19-SEP-2010','DD-MON-YYYY'), 101, TO_DATE('20-SEP-2010','DD-MON-YYYY'));
INSERT INTO rental_history (media_id, rental_date, customer_id, return_date) VALUES (93, TO_DATE('01-OCT-2010','DD-MON-YYYY'), 102, TO_DATE('05-OCT-2010','DD-MON-YYYY'));
INSERT INTO rental_history (media_id, rental_date, customer_id, return_date) VALUES (94, TO_DATE('12-OCT-2010','DD-MON-YYYY'), 103, NULL);
INSERT INTO rental_history (media_id, rental_date, customer_id, return_date) VALUES (95, TO_DATE('20-OCT-2010','DD-MON-YYYY'), 104, TO_DATE('22-OCT-2010','DD-MON-YYYY'));
COMMIT;

SELECT * FROM customers;
SELECT * FROM movies;
SELECT * FROM media;
SELECT * FROM actors;
SELECT * FROM star_billings;
SELECT * FROM rental_history;

SELECT * FROM title_unavail;

/* 6. Create Indexes */
CREATE INDEX customers_last_name_idx ON customers(last_name);

SELECT index_name, table_name, status FROM user_indexes WHERE table_name = 'CUSTOMERS';
SELECT index_name, column_name, column_position FROM user_ind_columns WHERE table_name = 'CUSTOMERS' ORDER BY index_name, column_position;

/* 7. Create Synonyms */
CREATE SYNONYM tu FOR title_unavail;

SELECT synonym_name, table_owner, table_name FROM user_synonyms WHERE synonym_name = 'TU';
SELECT * FROM tu;