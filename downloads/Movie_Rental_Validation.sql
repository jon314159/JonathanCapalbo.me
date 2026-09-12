SET SERVEROUTPUT ON SIZE UNLIMITED
SET FEEDBACK ON
SET VERIFY OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK

DECLARE
  passed PLS_INTEGER := 0;
  result NUMBER;
  PROCEDURE equal_count(label VARCHAR2, statement VARCHAR2, expected NUMBER) IS
    actual NUMBER;
  BEGIN
    EXECUTE IMMEDIATE statement INTO actual;
    IF actual != expected OR actual IS NULL THEN
      RAISE_APPLICATION_ERROR(-20001, label || ': expected ' || expected || ', got ' || actual);
    END IF;
    passed := passed + 1;
    DBMS_OUTPUT.PUT_LINE('PASS | ' || label || ' | ' || actual);
  END;
  PROCEDURE rejects(label VARCHAR2, statement VARCHAR2, expected_code NUMBER) IS
    actual_code NUMBER := 0;
  BEGIN
    SAVEPOINT validation_case;
    BEGIN
      EXECUTE IMMEDIATE statement;
    EXCEPTION WHEN OTHERS THEN actual_code := SQLCODE;
    END;
    ROLLBACK TO validation_case;
    IF actual_code != expected_code THEN
      RAISE_APPLICATION_ERROR(-20002, label || ': expected Oracle code ' || expected_code || ', got ' || actual_code);
    END IF;
    passed := passed + 1;
    DBMS_OUTPUT.PUT_LINE('PASS | ' || label || ' | Oracle code ' || actual_code);
  END;
  PROCEDURE advances(label VARCHAR2, sequence_name VARCHAR2, table_name VARCHAR2, key_name VARCHAR2) IS
    highest_id NUMBER;
    first_id NUMBER;
    second_id NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'SELECT MAX(' || key_name || ') FROM ' || table_name INTO highest_id;
    EXECUTE IMMEDIATE 'SELECT ' || sequence_name || '.NEXTVAL FROM dual' INTO first_id;
    EXECUTE IMMEDIATE 'SELECT ' || sequence_name || '.NEXTVAL FROM dual' INTO second_id;
    IF first_id <= highest_id OR second_id <= first_id THEN
      RAISE_APPLICATION_ERROR(-20003, label || ': sequence failed to generate new increasing IDs');
    END IF;
    passed := passed + 1;
    DBMS_OUTPUT.PUT_LINE('PASS | ' || label || ' | maximum stored ' || highest_id || ', next IDs ' || first_id || ', ' || second_id);
  END;
BEGIN
  equal_count('Customer rows', 'SELECT COUNT(*) FROM customers', 6);
  equal_count('Movie rows', 'SELECT COUNT(*) FROM movies', 6);
  equal_count('Media rows', 'SELECT COUNT(*) FROM media', 8);
  equal_count('Actor rows', 'SELECT COUNT(*) FROM actors', 4);
  equal_count('Casting rows', 'SELECT COUNT(*) FROM star_billings', 4);
  equal_count('Rental rows', 'SELECT COUNT(*) FROM rental_history', 4);
  equal_count('Expected tables', q'[SELECT COUNT(*) FROM user_tables WHERE table_name IN ('CUSTOMERS','MOVIES','MEDIA','ACTORS','STAR_BILLINGS','RENTAL_HISTORY')]', 6);
  equal_count('Enabled primary keys', q'[SELECT COUNT(*) FROM user_constraints WHERE constraint_type='P' AND status='ENABLED' AND validated='VALIDATED' AND table_name IN ('CUSTOMERS','MOVIES','MEDIA','ACTORS','STAR_BILLINGS','RENTAL_HISTORY')]', 6);
  equal_count('Enabled foreign keys', q'[SELECT COUNT(*) FROM user_constraints WHERE constraint_type='R' AND status='ENABLED' AND validated='VALIDATED' AND table_name IN ('MEDIA','STAR_BILLINGS','RENTAL_HISTORY')]', 5);
  equal_count('Enabled rating/category checks', q'[SELECT COUNT(*) FROM user_constraints WHERE constraint_name IN ('MOVIES_RATING_CK','MOVIES_CATEGORY_CK') AND status='ENABLED' AND validated='VALIDATED']', 2);
  equal_count('No invalid project objects', q'[SELECT COUNT(*) FROM user_objects WHERE status='INVALID' AND object_name IN ('CUSTOMERS','MOVIES','MEDIA','ACTORS','STAR_BILLINGS','RENTAL_HISTORY','TITLE_UNAVAIL','CUSTOMERS_SEQ','MOVIES_SEQ','MEDIA_SEQ','ACTORS_SEQ','CUSTOMERS_LAST_NAME_IDX','TU')]', 0);
  equal_count('Unreturned copies', 'SELECT COUNT(*) FROM title_unavail', 1);
  equal_count('Correct unreturned copy', q'[SELECT COUNT(*) FROM title_unavail WHERE media_id=94 AND title='The Shawshank Redemption']', 1);
  equal_count('Synonym result', q'[SELECT COUNT(*) FROM tu WHERE media_id=94 AND title='The Shawshank Redemption']', 1);
  equal_count('Synonym resolves in this schema', q'[SELECT COUNT(*) FROM user_synonyms WHERE synonym_name='TU' AND table_name='TITLE_UNAVAIL' AND table_owner=USER]', 1);
  equal_count('Explicit index exists and is valid', q'[SELECT COUNT(*) FROM user_indexes WHERE index_name='CUSTOMERS_LAST_NAME_IDX' AND table_name='CUSTOMERS' AND status='VALID']', 1);
  equal_count('Index targets last_name', q'[SELECT COUNT(*) FROM user_ind_columns WHERE index_name='CUSTOMERS_LAST_NAME_IDX' AND column_name='LAST_NAME' AND column_position=1]', 1);
  equal_count('Four sequences with unit increments', q'[SELECT COUNT(*) FROM user_sequences WHERE sequence_name IN ('CUSTOMERS_SEQ','MOVIES_SEQ','MEDIA_SEQ','ACTORS_SEQ') AND increment_by=1]', 4);
  advances('Customers sequence generates new IDs', 'customers_seq', 'customers', 'customer_id');
  advances('Movies sequence generates new IDs', 'movies_seq', 'movies', 'title_id');
  advances('Media sequence generates new IDs', 'media_seq', 'media', 'media_id');
  advances('Actors sequence generates new IDs', 'actors_seq', 'actors', 'actor_id');

  rejects('Duplicate customer key', 'INSERT INTO customers SELECT * FROM customers WHERE customer_id=101', -1);
  rejects('Duplicate movie key', 'INSERT INTO movies SELECT * FROM movies WHERE title_id=1', -1);
  rejects('Duplicate media key', 'INSERT INTO media SELECT * FROM media WHERE media_id=92', -1);
  rejects('Duplicate actor key', 'INSERT INTO actors SELECT * FROM actors WHERE actor_id=1001', -1);
  rejects('Duplicate casting key', 'INSERT INTO star_billings SELECT * FROM star_billings WHERE title_id=2 AND actor_id=1001', -1);
  rejects('Duplicate rental key', 'INSERT INTO rental_history SELECT * FROM rental_history WHERE media_id=92', -1);
  rejects('Missing required name', 'UPDATE customers SET first_name=NULL WHERE customer_id=101', -1407);
  rejects('Media needs an existing movie', q'[INSERT INTO media VALUES (99999, -999, 'DVD')]', -2291);
  rejects('Casting needs an existing movie', q'[INSERT INTO star_billings VALUES (-999, 1001, 'Test')]', -2291);
  rejects('Casting needs an existing actor', q'[INSERT INTO star_billings VALUES (1, -999, 'Test')]', -2291);
  rejects('Rental needs existing media', q'[INSERT INTO rental_history VALUES (-999,101,DATE '2011-01-01',NULL)]', -2291);
  rejects('Rental needs an existing customer', q'[INSERT INTO rental_history VALUES (92,-999,DATE '2011-01-01',NULL)]', -2291);
  rejects('Referenced movie cannot be deleted', 'DELETE FROM movies WHERE title_id=1', -2292);
  rejects('Invalid rating rejected', q'[UPDATE movies SET rating='X' WHERE title_id=1]', -2290);
  rejects('Invalid category rejected', q'[UPDATE movies SET category='UNKNOWN' WHERE title_id=1]', -2290);
  rejects('Read-only view rejects writes', 'DELETE FROM title_unavail WHERE media_id=94', -42399);

  SAVEPOINT before_return;
  UPDATE rental_history SET return_date=DATE '2010-10-14' WHERE media_id=94;
  equal_count('Returning a copy updates the view', 'SELECT COUNT(*) FROM title_unavail', 0);
  equal_count('Returning a copy updates the synonym', 'SELECT COUNT(*) FROM tu', 0);
  ROLLBACK TO before_return;

  SAVEPOINT before_default;
  INSERT INTO rental_history (media_id,customer_id) VALUES (99,101);
  equal_count('Rental date defaults to current time', 'SELECT COUNT(*) FROM rental_history WHERE media_id=99 AND rental_date BETWEEN SYSDATE-1/1440 AND SYSDATE', 1);
  ROLLBACK TO before_default;
  equal_count('Rental test rows rolled back', 'SELECT COUNT(*) FROM rental_history', 4);
  equal_count('View restored after tests', 'SELECT COUNT(*) FROM title_unavail', 1);
  DBMS_OUTPUT.PUT_LINE('CORE_VALIDATION_PASSED | ' || passed || ' checks');

  -- These probes document rules the assignment does not enforce; they do not assert assignment failures.
  SAVEPOINT before_probe;
  UPDATE rental_history SET return_date=rental_date-1 WHERE media_id=92;
  DBMS_OUTPUT.PUT_LINE('LIMITATION CONFIRMED | A return earlier than its rental is accepted.');
  ROLLBACK TO before_probe;

  SAVEPOINT before_probe;
  INSERT INTO rental_history (media_id,customer_id,rental_date,return_date)
    VALUES (94,101,DATE '2010-10-13',NULL);
  SELECT COUNT(*) INTO result FROM title_unavail WHERE media_id=94;
  DBMS_OUTPUT.PUT_LINE('LIMITATION CONFIRMED | Multiple open rentals for one copy are accepted; view rows for media 94: ' || result);
  ROLLBACK TO before_probe;

  SAVEPOINT before_probe;
  UPDATE movies SET rating=NULL WHERE title_id=1;
  DBMS_OUTPUT.PUT_LINE('DESIGN BEHAVIOR | A NULL rating is allowed.');
  ROLLBACK TO before_probe;
END;
/
ROLLBACK;
