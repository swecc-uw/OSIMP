# OSIMP Server

## What is this?

A server meant to be maintained by the mock interview program manager. It will convienently handle the pairing of people that signed up for the mock interview program, writing them to both a database and local file cache.

## How do I run?

### Change directory to the server folder:

```bash
cd server
```

### Install dependencies:

```bash
pip3 install -r requirements.txt
```

### Create a `.env` file using `.env.sample` file

### Set up database from `migration/setup_db.sql`

### Run the following commands:
```bash
python3 server.py
```

## Endpoints

Visit [docs](http://localhost:8080/docs) while your local server is running.
