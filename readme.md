# Udacity Project 4: Tournament Results

##
This is a simple database project using Python and [PostgreSQL](https://www.postgresql.org/download/).


### Installation with VirtualBox/Vagrant
[Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) are used to create a consistent development environment. [Udacity Vagrant Wiki](https://www.udacity.com/wiki/ud197/install-vagrant)

Fork an clone the [Udacity starter repo](https://github.com/udacity/fullstack-nanodegree-vm)

Clone/download this [repo](https://github.com/screamingjungle/Portfolio-FSWD-Project4-Tournament) into the /vagrant directory. in the \vagrant directory `vagrant up` will configure and provision your environment. Connect to the environment using `vagrant ssh` (ssh may need to configured in your console/terminal - Git Bash has ssh support).

When successful, you should be logged in as

`vagrant@vagrant-ubuntu-trusty-32:~$ `

From there, do `cd /vagrant` to see the project files.

### Installation without VirtualBox/Vagrant

Clone or Download this [repo](https://github.com/screamingjungle/Portfolio-FSWD-Project4-Tournament)

You will need Python and PostgreSQL installed.

### Tournament Database
The tournament database is defined in the tournament.sql file. From within the /tournament directory, type `psql` in the terminal. Then, type `\i tournament.sql`. This will run the tournament.sql file, and create the tournament database. `Ctrl-D` or `\q` to quit.

To recreate the database you may need to restart the PostgreSQL service to clear connections (e.g. `sudo service postgresql restart`).

### Tournament test
`python tournament_test.py` in your terminal to run a series of tests. A successful test will show the following:

```python
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!

```