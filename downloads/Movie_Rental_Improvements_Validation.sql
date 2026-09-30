-- Run after the original project and Movie_Rental_Improvements.sql in a fresh schema.
-- Row changes are rolled back; no production database or customer data is needed.
SET SERVEROUTPUT ON SIZE UNLIMITED
SET FEEDBACK ON
SET VERIFY OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK

DECLARE
  passed PLS_INTEGER := 0;
  PROCEDURE equal_count(label VARCHAR2, statement VARCHAR2, expected NUMBER) IS
    actual NUMBER;
  BEGIN
    EXECUTE IMMEDIATE statement INTO actual;
    IF actual IS NULL OR actual != expected THEN
      RAISE_APPLICATION_ERROR(-20001, label || ': expected ' || expected || ', got ' || actual);
    END IF;
    passed := passed + 1;
    DBMS_OUTPUT.PUT_LINE('PASS | ' || label || ' | ' || actual);
  END;
  PROCEDURE rejects(label VARCHAR2, statement VARCHAR2, expected_code NUMBER) IS
    actual_code NUMBER := 0;
  BEGIN
    SAVEPOINT invalid_case;
    BEGIN
      EXECUTE IMMEDIATE statement;
    EXCEPTION WHEN OTHERS THEN actual_code := SQLCODE;
    END;
    ROLLBACK TO invalid_case;
    IF actual_code != expected_code THEN
      RAISE_APPLICATION_ERROR(-20002, label || ': expected Oracle code ' || expected_code || ', got ' || actual_code);
    END IF;
    passed := passed + 1;
    DBMS_OUTPUT.PUT_LINE('PASS | ' || label || ' | Oracle code ' || actual_code);
  END;
BEGIN
  equal_count('Date-order constraint enabled and validated', q'[SELECT COUNT(*) FROM user_constraints WHERE constraint_name='RENTAL_RETURN_ORDER_CK' AND status='ENABLED' AND validated='VALIDATED']', 1);
  equal_count('Conditional unique index valid', q'[SELECT COUNT(*) FROM user_indexes WHERE index_name='RENTAL_ONE_OPEN_UQ' AND uniqueness='UNIQUE' AND status='VALID']', 1);
  equal_count('Original rental rows preserved', 'SELECT COUNT(*) FROM rental_history', 4);
  equal_count('Original open copy preserved', 'SELECT COUNT(*) FROM title_unavail WHERE media_id=94', 1);

  rejects('Insert rejects a return before checkout', q'[INSERT INTO rental_history VALUES (92,101,DATE '2011-01-02',DATE '2011-01-01')]', -2290);
  rejects('Update rejects a return before checkout', 'UPDATE rental_history SET return_date=rental_date-1 WHERE media_id=92', -2290);
  rejects('Moving checkout past its return is rejected', 'UPDATE rental_history SET rental_date=return_date+1 WHERE media_id=92', -2290);
  rejects('Second open rental for the same copy is rejected', q'[INSERT INTO rental_history VALUES (94,101,DATE '2011-01-01',NULL)]', -1);

  SAVEPOINT valid_cases;
  INSERT INTO rental_history VALUES (92,101,DATE '2011-01-01',DATE '2011-01-01');
  equal_count('Same-time checkout and return accepted', q'[SELECT COUNT(*) FROM rental_history WHERE media_id=92 AND rental_date=DATE '2011-01-01' AND return_date=rental_date]', 1);
  INSERT INTO rental_history VALUES (92,102,DATE '2011-01-02',DATE '2011-01-03');
  equal_count('Multiple completed rentals for one copy accepted', 'SELECT COUNT(*) FROM rental_history WHERE media_id=92 AND return_date IS NOT NULL', 3);
  INSERT INTO rental_history VALUES (92,101,DATE '2011-01-04',NULL);
  equal_count('Different copies can each have an open rental', 'SELECT COUNT(*) FROM title_unavail', 2);
  rejects('Reopening history while a copy is out is rejected', q'[UPDATE rental_history SET return_date=NULL WHERE media_id=92 AND rental_date=DATE '2011-01-02']', -1);
  rejects('Moving an open rental onto an occupied copy is rejected', q'[UPDATE rental_history SET media_id=94 WHERE media_id=92 AND rental_date=DATE '2011-01-04']', -1);
  UPDATE rental_history SET return_date=DATE '2011-01-05' WHERE media_id=92 AND return_date IS NULL;
  equal_count('Returning a copy removes it from availability view', 'SELECT COUNT(*) FROM title_unavail WHERE media_id=92', 0);
  INSERT INTO rental_history VALUES (92,102,DATE '2011-01-06',NULL);
  equal_count('A returned copy can be rented again', 'SELECT COUNT(*) FROM title_unavail WHERE media_id=92', 1);
  equal_count('Synonym reflects the new open rental', 'SELECT COUNT(*) FROM tu WHERE media_id=92', 1);
  equal_count('Open-copy view has no duplicate copies', 'SELECT COUNT(*)-COUNT(DISTINCT media_id) FROM title_unavail', 0);
  ROLLBACK TO valid_cases;
  equal_count('Validation restores original rental rows', 'SELECT COUNT(*) FROM rental_history', 4);
  equal_count('Validation restores original view result', 'SELECT COUNT(*) FROM title_unavail WHERE media_id=94', 1);
  equal_count('No date-order violations remain', 'SELECT COUNT(*) FROM rental_history WHERE return_date < rental_date', 0);
  DBMS_OUTPUT.PUT_LINE('IMPROVEMENT_VALIDATION_PASSED | ' || passed || ' checks');
END;
/
ROLLBACK;
