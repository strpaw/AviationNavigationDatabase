CREATE TABLE abbreviation (
    abbr_id serial PRIMARY KEY,
    abbrev VARCHAR(20) NOT NULL,
    term VARCHAR(300) NOT NULL,
    user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL
);

CREATE TABLE country (
    ctry_id SERIAL PRIMARY KEY,
    iso_alpha3 CHAR(3) NOT NULL UNIQUE,
    official_name VARCHAR(150) NOT NULL,
    short_name VARCHAR(75) NOT NULL,
    ais_www VARCHAR(50) NULL,
    user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL,
    boundary GEOGRAPHY(MULTIPOLYGON, 4326)
);

CREATE TABLE obstacle_type (
    obst_type_id SMALLSERIAL PRIMARY KEY,
    obst_type VARCHAR(45) NOT NULL
);

CREATE TABLE obstacle (
    obst_id SERIAL PRIMARY KEY,
    ctry_id INT NOT NULL,
    obst_identifier VARCHAR(35),
    obst_name VARCHAR(100) NULL,
    lon_src VARCHAR(30) NOT NULL,
    lat_src VARCHAR(30) NOT NULL,
    agl FLOAT NULL,
    amsl FLOAT NOT NULL,
    vert_uom VARCHAR(2) NULL,
    hor_acc FLOAT NULL,
    hor_acc_uom VARCHAR(2) NULL,
    vert_acc FLOAT NULL,
    vert_acc_uom VARCHAR(2) NULL,
    obst_type_id INT NOT NULL,
    lighting CHAR(1) NOT NULL DEFAULT 'U',
    marking CHAR(1) NOT NULL DEFAULT 'U',
    is_group BOOLEAN NOT NULL DEFAULT FALSE,
    user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL,
    obst_location GEOGRAPHY(POINT, 4326),
    CONSTRAINT fk_obst_ctry FOREIGN KEY (ctry_id) REFERENCES country(ctry_id),
    CONSTRAINT fk_obst_obst_type FOREIGN KEY (obst_type_id) REFERENCES obstacle_type(obst_type_id),
    CONSTRAINT check_agl_positive CHECK (agl > 0),
    CONSTRAINT check_lighting_valid CHECK (lighting IN ('Y', 'N', 'U')),
    CONSTRAINT check_marking_valid CHECK (marking IN ('Y', 'N', 'U'))
);

CREATE TABLE fir (
	fir_ident CHAR(4) PRIMARY KEY,
	ctry_id INT NOT NULL,
	fir_name VARCHAR(150) NOT NULL,
	lower_limit FLOAT NOT NULL,
	lower_limit_uom VARCHAR(2) NOT NULL,
	upper_limit FLOAT NOT NULL NOT NULL,
	upper_limit_uom VARCHAR(2) NOT NULL,
	activity_time VARCHAR(300) NOT NULL,
	user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL,
	lateral_limits_text VARCHAR(4000),
	fir_boundary GEOGRAPHY (POLYGON, 4326),
	CONSTRAINT fk_fir_ctry FOREIGN KEY (ctry_id) REFERENCES country(ctry_id)
);

CREATE TABLE fir_class (
	fir_class_id SERIAL PRIMARY KEY,
	fir_ident CHAR(4) NOT NULL,
	lower_limit FLOAT NOT NULL,
	lower_limit_uom VARCHAR(2) NOT NULL,
	upper_limit FLOAT NOT NULL NOT NULL,
	upper_limit_uom VARCHAR(2) NOT NULL,
	asp_class CHAR(1) NOT NULL,
	CONSTRAINT fk_fir_class_fir FOREIGN KEY (fir_ident) REFERENCES fir(fir_ident)
);

CREATE TABLE airspace (
    asp_id SERIAL PRIMARY KEY,
    fir_ident CHAR(4) NOT NULL,
    asp_ident VARCHAR(30) NOT NULL,
    asp_name VARCHAR(150) NULL,
    asp_type VARCHAR(50) NOT NULL,
    lower_limit FLOAT NOT NULL,
    lower_limit_uom VARCHAR(2) NOT NULL,
    upper_limit FLOAT NOT NULL NOT NULL,
    upper_limit_uom VARCHAR(2) NOT NULL,
    lateral_limits_text VARCHAR(4000),
    user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL,
    asp_boundary GEOGRAPHY (POLYGON, 4326),
    CONSTRAINT check_unique_asp_ident UNIQUE (fir_ident, asp_ident)
);

CREATE TABLE asp_class (
    asp_class_id SERIAL PRIMARY KEY,
    asp_id INT NOT NULL,
    lower_limit FLOAT NOT NULL,
    lower_limit_uom VARCHAR(2) NOT NULL,
    upper_limit FLOAT NOT NULL NOT NULL,
    upper_limit_uom VARCHAR(2) NOT NULL,
    asp_class CHAR(1) NOT NULL,
	CONSTRAINT fk_asp_class_asp FOREIGN KEY (asp_id) REFERENCES airspace(asp_id)
);

CREATE TABLE waypoint (
    wpt_id SERIAL PRIMARY KEY,
    wpt_ident VARCHAR(5) NOT NULL,
    fir_ident CHAR(4) NOT NULL,
    lon_src VARCHAR(30) NOT NULL,
    lat_src VARCHAR(30) NOT NULL,
    mag_var VARCHAR(10) NULL,
    wpt_location GEOGRAPHY (POINT, 4326),
    CONSTRAINT fk_waypoint_fir FOREIGN KEY (fir_ident) REFERENCES fir(fir_ident),
    CONSTRAINT check_wpt_ident_unique UNIQUE(fir_ident, wpt_ident)
);

CREATE TABLE airport (
    airport_id INT PRIMARY KEY,
    iata_code CHAR(3) NULL,
    arp_elev FLOAT NOT NULL,
    arp_elev_uom VARCHAR(2) NOT NULL,
    operational_hours VARCHAR(300) NULL,
    fuel_types VARCHAR(200) NULL,
    fire_fighting_category VARCHAR(5) NULL,
    landing_facility_type VARCHAR(20) NOT NULL,
    city VARCHAR(50) NULL,
    short_name VARCHAR(50) NULL,
    user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL,
    CONSTRAINT fk_airport_waypoint FOREIGN KEY (airport_id) REFERENCES waypoint(wpt_id)
);

CREATE TABLE obstacle_airport (
    obst_id INT NOT NULL,
    airport_id INT NOT NULL,
    CONSTRAINT pk_obstacle_airport PRIMARY KEY (obst_id, airport_id),
    CONSTRAINT fk_oa_obstacle FOREIGN KEY (obst_id) REFERENCES obstacle(obst_id),
    CONSTRAINT fk_oa_airport FOREIGN KEY (airport_id) REFERENCES airport(airport_id)
);

CREATE TABLE taxiway (
    taxiway_id SERIAL PRIMARY KEY,
    airport_id INT NOT NULL,
    taxiway_name VARCHAR(10) NOT NULL,
    width FLOAT NOT NULL,
    width_uom VARCHAR(2) NOT NULL,
    surface VARCHAR(30) NOT NULL,
    pcn VARCHAR(30) NOT NULL,
    lighting VARCHAR(30) NULL,
    remarks VARCHAR(100) NULL,
    user_add CHAR(8) DEFAULT current_user,
    timestamp_add TIMESTAMP DEFAULT now(),
    user_mod CHAR(8) NULL,
    timestamp_mod TIMESTAMP NULL,
    CONSTRAINT fk_taxiway_airport FOREIGN KEY (airport_id) REFERENCES airport(airport_id)
);
