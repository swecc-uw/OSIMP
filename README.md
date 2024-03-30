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

### Create a `.env` file with the following contents:

```bash
PAIRING_SECRET=your_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Run the following commands:

```bash
python3 server.py
```

## Endpoints

Visit [http://0.0.0.0:8080/docs](docs) while your local server is running.
