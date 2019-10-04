-- Creates "master user for the database"
CREATE DATABASE tictac_db;
CREATE USER 'dbserver'@'%' IDENTIFIED BY 'db_pw';
GRANT ALL PRIVILEGES ON tictac_db.* TO 'dbserver'@'%';

-- Create user for the game server, with row-level read/write privileges
CREATE USER 'gameserver'@'%' IDENTIFIED BY 'game_pw';
GRANT SELECT, INSERT, UPDATE ON tictac_db.* TO 'gameserver'@'%';

-- Create user for the web server, with read-only privileges
CREATE USER 'webserver'@'%' IDENTIFIED BY 'web_pw';
GRANT SELECT ON tictac_db.* TO 'webserver'@'%';

USE tictac_db;

-- Very simply, creates a new table to house player data
CREATE TABLE players (
    id VARCHAR(40),
    win INT DEFAULT 0 NOT NULL,
    loss INT DEFAULT 0 NOT NULL,
    draw INT DEFAULT 0 NOT NULL,
    PRIMARY KEY (id)
);
