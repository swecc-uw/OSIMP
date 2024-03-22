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

| Path | Method | Parameters | Response | Description |
| --- | --- | --- | --- | --- |
| `/startjob` | POST | `secret` | `200` | Start the pairing job |
| `/status` | GET | none | `200` | Get the status of the pairing job |
| `/pairs` | GET | none | `200` | Get the pairs, or notify of cache miss |
| `/unpaired` | GET | none | `200` | Get the unpaired, or notify of cache miss |