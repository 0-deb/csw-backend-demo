#!/bin/bash

PROJECTDIR=pwd
echo -e -n "[*] Enter Username for DB:  "
read -r user

echo -e -n "[*] Enter Password for DB:  "
read -r password

echo -e -n "[*] Enter Database Schema Name:  "
read -r db


# Install PostgreSQL
# NOTE: Version (PostgreSQL) 12.1 (Debian 12.1-2)
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

yes | sudo apt-get update
yes | sudo apt install postgresql postgresql-contrib

#Start PostgreSQL service
sudo service postgresql restart

# Installing python deoendencies
sudo pip3 install -r requirements.txt

# Setup DB password & permissions
sudo -u postgres psql << EOF

DROP DATABASE $db;
CREATE DATABASE $db;
CREATE USER $user WITH PASSWORD '$password';

ALTER ROLE $user SET client_encoding TO 'utf8';
ALTER ROLE $user SET default_transaction_isolation TO 'read committed';
ALTER ROLE $user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE $db TO $user;

EOF

# Setup DB Schema 
sudo python3 manage.py migrate --run-syncdb