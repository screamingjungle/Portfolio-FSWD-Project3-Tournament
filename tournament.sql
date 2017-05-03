-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drops tournament database if it exists
drop database if exists tournament;

-- Creates tournament database
create database tournament;

-- Connect to the tournament database
\c tournament

-- Create the players table for tracking players stats.
create table players(
    id serial primary key,
    name text);

-- Create the matches table for tracking matches.
create table matches(
    id serial primary key,
    winner integer references players(id),
    loser integer references players(id));

-- Create Standings View
create view view_standings as
    select 
        players.id, 
        players.name, 
        sum(case when matches.winner = players.id then 1 else 0 end) as wins,
        count(matches.id) as matches
    from players 
    left join matches on 
        players.id in (winner, loser)
    group by 
        players.id
    order by 
        wins desc;
