/* Separate AI-assisted portfolio extension, September 2026.
   Run once after Movie_Rental_Database.sql in a disposable Oracle schema.
   The academic submission is unchanged. Oracle DDL commits implicitly.
   Existing violations must be resolved before applying these rules.
*/
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK

ALTER TABLE rental_history ADD CONSTRAINT rental_return_order_ck
  CHECK (return_date IS NULL OR return_date >= rental_date);

-- Completed rentals map to NULL, allowing repeated historical rentals per copy.
CREATE UNIQUE INDEX rental_one_open_uq ON rental_history
  (CASE WHEN return_date IS NULL THEN media_id ELSE NULL END);

PROMPT Rental date-order and one-open-rental rules installed.
