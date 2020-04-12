/* Version 0.1 */

/*
Table: country
Statement: DDL
Country basic information
*/

CREATE TABLE country (
    rec_id serial PRIMARY KEY, -- Record ID
    ctry_iso3 char(3) NOT NULL, -- Three letter country ISO code
    ctry_short_name varchar(50) NOT NULL,
    ctry_official_name varchar(150) NULL,
    ais_html varchar(50) NULL,
    geo_location geography(POLYGON, 4326) NOT NULL
)

-- Significant waypoint table

/*
Table: sig_waypoint
Statement: DDL
Stores significant waypoints
*/
DROP TABLE IF EXISTS sig_waypoint;
CREATE TABLE sig_waypoint (
    rec_id serial PRIMARY KEY, -- Record ID
    ctry_iso3 char(3) NOT NULL, -- Three letter country ISO code
    wpt_ident varchar(30) NOT NULL, -- Waypoint name (ident)
    lon_src varchar(30) NOT NULL, -- Longitude from source
    lat_src varchar(30) NOT NULL, -- Latitude from source
    ins_user varchar(30) DEFAULT current_user NOT NULL, -- Insert: user name
    ins_tmsp timestamp DEFAULT now() NOT NULL, -- Insert: timestamp
    location geography(POINT, 4326) NOT NULL,
    CONSTRAINT sig_wpt_ctry_fk FOREIGN KEY (ctry_iso3) REFERENCES country (ctry_iso3)
);

/*
Table: etod
Statement: DDL
Stores Electronic Terrain and Obstacle Data (eTOD)
*/

DROP TABLE IF EXISTS etod;
CREATE TABLE etod (
    rec_id serial PRIMARY KEY, -- Record ID
    ctry_iso3 char(3) NOT NULL, -- Three letter country ISO code
    obst_id varchar(50) NOT NULL, -- Obstacle ident
    obst_type varchar(20) NOT NULL, -- Obstacle type
    lon_src varchar(30) NOT NULL, -- Longitude from source
    lat_src varchar(30) NOT NULL, -- Latitude from source
    amsl float NOT NULL, -- Elevation
    agl float NOT NULL, -- Height above ground
    vert_uom varchar(2) NOT NULL, -- Vertical unit of measure
    lighting char(20) NOT NULL, -- Lighting information
    marking char(20) NOT NULL, -- Marking information
    ins_user varchar(30) NOT NULL DEFAULT current_user , -- Insert: user name
    ins_tmsp timestamp NOT NULL DEFAULT now(), -- Insert: timestamp
    last_mod_user varchar(30) NULL, -- Modification: user name
    last_mod_tmsp timestamp NULL, -- Modification: timestamp
    geo_location geography(POINT, 4326) NOT NULL,
    CONSTRAINT valid_agl CHECK (agl > 0),
    CONSTRAINT valid_vert_uom CHECK (vert_uom IN ('ft', 'm')),
--    CONSTRAINT valid_lighting CHECK (lighting IN ('Y', 'N', 'U')),
--    CONSTRAINT valid_marking CHECK (marking IN ('Y', 'N', 'U'))
    CONSTRAINT etod_ctry_fk FOREIGN KEY (ctry_iso3) REFERENCES country (ctry_iso3)
);


CREATE OR REPLACE FUNCTION etod_update_mod_data()
    RETURNS trigger as
$BODY$
begin
    new.last_mod_user = (select current_user);
    new.last_mod_tmsp=now();
    return new;
end;
$BODY$
language PLPGSQL;

CREATE TRIGGER etod_mod
    BEFORE UPDATE
    ON etod
    FOR EACH ROW
    EXECUTE PROCEDURE etod_update_mod_data();