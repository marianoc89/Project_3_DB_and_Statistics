-- 1) Creating the Dtabase that will be used to load data from Python
DROP DATABASE IF EXISTS futbol;
CREATE DATABASE futbol;
-- 2) Tables created and uploaded from Python
-- 3) Altering tables to assign correct datatypes, Primary Keys and Foreign Keys:
ALTER TABLE league_results_table 
MODIFY COLUMN Rank INT(11),
MODIFY COLUMN Club VARCHAR(255) PRIMARY KEY,
MODIFY COLUMN `Partidos jugados` INT(11),
MODIFY COLUMN Victorias INT(11),
MODIFY COLUMN Empates INT(11),
MODIFY COLUMN Derrotas INT(11),
MODIFY COLUMN `Goles marcados` INT(11),
MODIFY COLUMN `Goles en contra` INT(11),
MODIFY COLUMN `Diferencia de goles` INT(11),
MODIFY COLUMN Puntos INT(11),
MODIFY COLUMN `Ultimo partido` VARCHAR(40),
MODIFY COLUMN `Ultimo partido -1` VARCHAR(40),
MODIFY COLUMN `Ultimo partido -2` VARCHAR(40),
MODIFY COLUMN `Ultimo partido -3` VARCHAR(40),
MODIFY COLUMN `Ultimo partido -4` VARCHAR(40);

ALTER TABLE upcoming_matches 
MODIFY COLUMN Fecha DATETIME,
MODIFY COLUMN Home VARCHAR(255),
MODIFY COLUMN vs VARCHAR(5),
MODIFY COLUMN Away VARCHAR(255),
MODIFY COLUMN `Time - League` VARCHAR(255),
MODIFY COLUMN `Match Number` INT(11) PRIMARY KEY;

ALTER TABLE historical_upcoming_matches 
MODIFY COLUMN Home VARCHAR(255),
MODIFY COLUMN Resultado VARCHAR(255),
MODIFY COLUMN Away VARCHAR(255),
MODIFY COLUMN Fecha DATETIME,
MODIFY COLUMN League VARCHAR(255),
MODIFY COLUMN `Match Number` INT(11),
MODIFY COLUMN River_Resultado VARCHAR(255);

ALTER TABLE field_players 
MODIFY COLUMN Nombre VARCHAR(255) PRIMARY KEY,
MODIFY COLUMN Posición VARCHAR(255),
MODIFY COLUMN Edad INT(11),
MODIFY COLUMN `Estatura (cm)` INT(11),
MODIFY COLUMN `Peso (kg)` INT(11),
MODIFY COLUMN Nacionalidad VARCHAR(255),
MODIFY COLUMN Apariciones INT(11),
MODIFY COLUMN Apariciones_Sustituto INT(11),
MODIFY COLUMN Goles INT(11),
MODIFY COLUMN Asistencias INT(11),
MODIFY COLUMN Tiros INT(11),
MODIFY COLUMN Tiros_Meta INT(11),
MODIFY COLUMN Faltas_cometidas INT(11),
MODIFY COLUMN Faltas_sufridas INT(11),
MODIFY COLUMN Tarjetas_amarillas INT(11),
MODIFY COLUMN Tarjetas_Rojas INT(11);

ALTER TABLE goal_keepers 
MODIFY COLUMN Nombre VARCHAR(255) PRIMARY KEY,
MODIFY COLUMN Posición VARCHAR(255),
MODIFY COLUMN Edad INT(11),
MODIFY COLUMN `Estatura (cm)` INT(11),
MODIFY COLUMN `Peso (kg)` INT(11),
MODIFY COLUMN Nacionalidad VARCHAR(255),
MODIFY COLUMN Apariciones INT(11),
MODIFY COLUMN Apariciones_Sustituto INT(11),
MODIFY COLUMN Atajadas INT(11),
MODIFY COLUMN Goles_Concedidos INT(11),
MODIFY COLUMN Asistencias INT(11),
MODIFY COLUMN Faltas_cometidas INT(11),
MODIFY COLUMN Faltas_sufridas INT(11),
MODIFY COLUMN Tarjetas_amarillas INT(11),
MODIFY COLUMN Tarjetas_Rojas INT(11);

-- Relationing historical_upcoming_matches with upcoming_matches
USE futbol;
ALTER TABLE historical_upcoming_matches
	ADD FOREIGN KEY (`Match Number`)
    REFERENCES upcoming_matches(`Match Number`)
    ON DELETE CASCADE;

-- 4) Check data by querying:
USE futbol;
SELECT *
FROM historical_upcoming_matches;

-- Checking joins between tables
USE futbol;
SELECT h.Fecha, h.Home, River_Resultado, `Time - League`
FROM historical_upcoming_matches h
JOIN upcoming_matches u ON h.`Match Number` = u.`Match Number`
WHERE u.`Match Number` = 1;

-- With clause is not compatible with this version of MySQL
-- Counting How many times River Won Away and Home...Home>Away
USE futbol;
DROP TEMPORARY TABLE IF EXISTS river_home;
CREATE TEMPORARY TABLE river_home AS (
SELECT COUNT(Home)
FROM historical_upcoming_matches
WHERE River_Resultado = 'Victoria'
AND Home = 'River Plate');
DROP TEMPORARY TABLE IF EXISTS river_away;
CREATE TEMPORARY TABLE river_away AS (
SELECT COUNT(Away)
FROM historical_upcoming_matches
WHERE River_Resultado = 'Victoria'
AND Away = 'River Plate'
);

SELECT *
FROM river_home,river_away