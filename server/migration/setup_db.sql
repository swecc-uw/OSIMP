DROP TABLE IF EXISTS email_notifications;

CREATE TABLE email_notifications (
    form_id INT NOT NULL,
    user_id UUID NOT NULL,
    contents TEXT NOT NULL,
    subject TEXT NOT NULL
);

DROP TABLE IF EXISTS unpaired;

CREATE TABLE unpaired (
    form_id INT NOT NULL,
    user_id UUID NOT NULL
);

DROP TABLE IF EXISTS pairs;

CREATE TABLE pairs (
    form_id INT NOT NULL,
    p1_id UUID NOT NULL,
    p2_id UUID NOT NULL
);

DROP TABLE IF EXISTS signups;

CREATE TABLE signups (
    created_at timestamp with time zone NOT NULL,
    form_id integer NOT NULL,
    availability jsonb NOT NULL,
    user_id uuid NOT NULL
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id uuid PRIMARY KEY,        -- Assuming user_id is a UUID and the primary key
    email varchar(255) NOT NULL,     -- Email address, assuming a max length of 255
    major varchar(255),              -- Major, assuming a max length of 255
    discord varchar(255),            -- Discord handle, assuming a max length of 255
    first_name varchar(255) NOT NULL,-- First name, assuming a max length of 255
    last_name varchar(255) NOT NULL, -- Last name, assuming a max length of 255
    grad_year integer                -- Graduation year, assuming it's an integer
);

DROP TABLE IF EXISTS forms;

CREATE TABLE forms (
    id serial PRIMARY KEY,
    created_at timestamp with time zone NOT NULL,
    state text NOT NULL,
);

DROP TABLE IF EXISTS problems;

CREATE TABLE problems (
    problem_url text NOT NULL,
    problem_number integer NOT NULL,
    seq integer NOT NULL,
    form_id integer NOT NULL,
    topic text NOT NULL
);
