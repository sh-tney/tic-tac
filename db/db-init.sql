-- Very simply, creates a new table to house player data
CREATE TABLE players (
    id VARCHAR(40),
    win INT DEFAULT 0 NOT NULL,
    loss INT DEFAULT 0 NOT NULL,
    draw INT DEFAULT 0 NOT NULL,
    PRIMARY KEY (id)
);