-- PandaVault schema (SQLite)
--
-- Reconstructed from how panda/vault.py uses each table (the original
-- MySQL DDL was never in this repo; it lived on the external server).
-- Run by init_db() on first launch. Ships with NO data: every table is
-- created empty, and each user fills their own vault.
--
-- Type choices follow SQLite's affinities (TEXT / INTEGER / REAL),
-- driven by actual code usage. PRIMARY KEYs are declared on the column
-- the code deletes/edits/dedups by.

CREATE TABLE IF NOT EXISTS Emergency (
    Patient_ID           TEXT PRIMARY KEY,   -- entered as a string; ordered/edited/deleted by this
    Name                 TEXT,
    Age                  INTEGER,            -- code does int(input(...))
    Blood_Group          TEXT,
    Chronic_Disease      TEXT,
    Doctor_Name          TEXT,
    Doctor_Phone         TEXT,               -- phone: keep as text (leading zeros / +)
    Allergic_Medications TEXT
);

CREATE TABLE IF NOT EXISTS Medicine (
    Disease       TEXT PRIMARY KEY,          -- edited/deleted by Disease
    Medicine_Name TEXT,
    Manufacturer  TEXT,
    Duration      TEXT,                       -- free text (e.g. "5 days")
    Quantity      INTEGER,
    Amount        REAL,                       -- money
    Remark        TEXT
);

CREATE TABLE IF NOT EXISTS Student_Marks (
    Exam_Name        TEXT PRIMARY KEY,        -- edited/deleted by Exam_Name
    Physics          INTEGER,
    Chemistry        INTEGER,
    Mathematics      INTEGER,
    English          INTEGER,
    Computer_Science INTEGER
    -- NOTE: MARKSHEET() computes Total/5 as Average. In SQLite,
    -- INTEGER/INTEGER is integer division, so the query (not the schema)
    -- must divide by 5.0 to keep decimals. Handled in Step 4.
);

