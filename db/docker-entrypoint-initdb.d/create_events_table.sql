CREATE TYPE EVENT_REPEAT_TYPE AS ENUM (
    'SINGLE_EVENT',
    'REPEAT_DAILY',
    'REPEAT_WEEKLY',
    'REPEAT_MONTHLY',
    'REPEAT_YEARLY',
    'REPEAT_WORKDAYS',
    'REPEAT_CUSTOM'
);

CREATE TABLE IF NOT EXISTS events (
   id TEXT PRIMARY KEY,
   created_by TEXT NOT NULL,
   invited TEXT[] NOT NULL,
   accepted TEXT[] NOT NULL,
   schedule_start TIMESTAMP NOT NULL,
   duration INTERVAL NOT NULL,
   is_private BOOLEAN NOT NULL,
   repeat_type EVENT_REPEAT_TYPE NOT NULL,
   description TEXT NOT NULL,
   custom_repeats_params JSON
);
