/ *

Table: sig_waypoint
DDL statement for table storing significant waypoints data
Version 0.1
*/

CREATE TABLE sig_waypoint (
    rec_id serial PRIMARY KEY, -- Record ID
    ctry_iso3 char(3) NOT NULL, -- Three letter country ISO code
    wpt_ident varchar(30) NOT NULL, -- Waypoint name (ident)
    lon_src varchar(30) NOT NULL, -- Longitude from source
    lat_src varchar(30) NOT NULL, -- Latitude from source
    ins_user varchar(30) DEFAULT current_user NOT NULL, -- Insert: user name
    ins_tmsp timestamp DEFAULT now() NOT NULL, -- Insert: timestamp
    location geography(POINT, 4326) NOT NULL
);
