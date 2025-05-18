CREATE TABLE users (
    id UUID PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    group_id UUID
);

CREATE TABLE groups (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_date TIMESTAMP NOT NULL,
    balance DOUBLE PRECISION NOT NULL
);

CREATE TABLE contributions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    group_id UUID NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    date TIMESTAMP NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE loans (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    group_id UUID NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    interest_rate DOUBLE PRECISION NOT NULL,
    date_issued TIMESTAMP NOT NULL,
    due_date TIMESTAMP NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE payouts (
    id UUID PRIMARY KEY,
    group_id UUID NOT NULL,
    user_id UUID NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    date TIMESTAMP NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE sync_queue (
    id UUID PRIMARY KEY,
    operation TEXT NOT NULL,
    entity TEXT NOT NULL,
    entity_id UUID NOT NULL,
    data TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);
