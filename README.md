# Official Repository for the Official Software Engineering Career Club Mock Interview Program

## What is this?

A collection of scripts that help manage the mock interview program. In particular, the following tasks are supported:

- Creating a new sign-up form
- Reading the responses from a sign-up form
- Creating pairs of interviewers and interviewees
- Sending emails to interviewers and interviewees

## How do I run?

First, you need credentials to access the forms API. If you are a member of SWECC and want to contribute, please contact me (Elijah Melton) and I'll get you set up.

Name your file `credentials.json` and place it in `./automation`. You should be able to do all the forms API stuff now.

To send emails, you'll need an additional secret file. Again, contact me (Elijah Melton) if you need this.

| Command | Description |
| --- | --- |
| `python3 create.py` | Create a new sign-up form |
| `python3 responses.py` | Read the responses from a sign-up form |
| `python3 pairs.py` | Create pairs of interviewers and interviewees |
| `python3 send.py` | Send emails to interviewers and interviewees |

