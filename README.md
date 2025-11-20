# CSCI 341 Assignment 3 - Caregivers Platform

Database management system connecting families with professional caregivers.

## Quick Start (Using Makefile)

```bash
make install

make db-local
make part2
make part3

make docker-start
make db-docker
make part2
make part3

make help
```

## Manual Setup

### Option 1: Local PostgreSQL

```bash
createdb caregivers_platform
psql caregivers_platform < caregivers_platform_part1.sql

pip install -r requirements.txt

python3 caregivers_platform_part2.py

python3 app.py
```


### Option 2: PostgreSQL with Docker


1. **Start PostgreSQL container**:
   ```bash
   docker run --name postgres-csci341 \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_USER=postgres \
     -p 5432:5432 \
     -d postgres:latest
   ```

2. **Create database and import data**:
   ```bash
   docker exec -it postgres-csci341 createdb -U postgres caregivers_platform
   docker exec -i postgres-csci341 psql -U postgres caregivers_platform < caregivers_platform_part1.sql
   ```

3. **Run the Python scripts**:
   ```bash
   pip install -r requirements.txt
   python3 caregivers_platform_part2.py
   python3 app.py
   ```

### If Docker Container Already Exists

```bash
# Start existing container
docker start postgres-csci341

# Import/reimport database
docker exec -i postgres-csci341 psql -U postgres caregivers_platform < caregivers_platform_part1.sql
```
