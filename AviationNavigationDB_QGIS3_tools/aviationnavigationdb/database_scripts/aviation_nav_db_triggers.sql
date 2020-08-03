CREATE OR REPLACE FUNCTION insert_mod_timestamp_user() RETURNS trigger as
/* Updates user_mod and timestamp_mod columns when row is modified */
$BODY$
begin
    new.user_mod = (select current_user);
    new.timestamp_mod = now();
    return new;
end;
$BODY$
language PLPGSQL;

CREATE TRIGGER abbreviation_mod
    BEFORE UPDATE
    ON abbreviation
    FOR EACH ROW
    EXECUTE PROCEDURE insert_mod_timestamp_user();

CREATE TRIGGER country_mod
    BEFORE UPDATE
    ON country
    FOR EACH ROW
    EXECUTE PROCEDURE insert_mod_timestamp_user();

CREATE TRIGGER obstacle_mod
    BEFORE UPDATE
    ON obstacle
    FOR EACH ROW
    EXECUTE PROCEDURE insert_mod_timestamp_user();

CREATE TRIGGER taxiway_mod
    BEFORE UPDATE
    ON taxiway
    FOR EACH ROW
    EXECUTE PROCEDURE insert_mod_timestamp_user();