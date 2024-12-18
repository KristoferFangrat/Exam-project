USE ROLE USERADMIN;

--- Creating roles
CREATE ROLE IF NOT EXISTS ExamDLTRole COMMENT = 'Role for data ingestion.';
CREATE ROLE IF NOT EXISTS ExamDBTRole COMMENT = 'Role for data transformation.';
CREATE ROLE IF NOT EXISTS ExamAnalystRole COMMENT = 'Role for data analysis.';

USE ROLE SECURITYADMIN;

--- Granting acces to warehouses
GRANT USAGE ON WAREHOUSE EXAM_WH TO ROLE ExamDLTRole;
GRANT USAGE ON WAREHOUSE EXAM_WH TO ROLE ExamDBTRole;
GRANT USAGE ON WAREHOUSE EXAM_WH TO ROLE ExamAnalystRole;

--- Granting acces to databases
GRANT USAGE ON DATABASE EXAM_DB TO ROLE ExamDLTRole;
GRANT USAGE ON DATABASE EXAM_DB TO ROLE ExamDBTRole;
GRANT USAGE ON DATABASE EXAM_DB TO ROLE ExamAnalystRole;

--- Granting acces to schemas
GRANT USAGE ON SCHEMA EXAM_DB.Staging1 TO ROLE ExamDLTRole;
GRANT USAGE ON SCHEMA EXAM_DB.Staging2 TO ROLE ExamDLTRole;

GRANT USAGE ON SCHEMA EXAM_DB.Staging1 TO ROLE ExamDBTRole;
GRANT USAGE ON SCHEMA EXAM_DB.Staging2 TO ROLE ExamDBTRole;

GRANT USAGE ON SCHEMA EXAM_DB.WAREHOUSE TO ROLE ExamDBTRole;

GRANT USAGE ON SCHEMA EXAM_DB.Mart1 TO ROLE ExamDBTRole;
GRANT USAGE ON SCHEMA EXAM_DB.Mart2 TO ROLE ExamDBTRole;

GRANT USAGE ON SCHEMA EXAM_DB.Mart1 TO ROLE ExamAnalystRole;
GRANT USAGE ON SCHEMA EXAM_DB.Mart2 TO ROLE ExamAnalystRole;

--- Granting select to tables
GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDLTRole;
GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Staging2 TO ROLE ExamDLTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDLTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Staging2 TO ROLE ExamDLTRole;

GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDBTRole;
GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Staging2 TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Staging2 TO ROLE ExamDBTRole;

--- Granting select on schema warehouse
GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Warehouse TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Warehouse TO ROLE ExamDBTRole;

GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamDBTRole;

GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamDBTRole;

GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamAnalystRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamAnalystRole;

GRANT SELECT ON ALL TABLES IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamAnalystRole;
GRANT SELECT ON FUTURE TABLES IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamAnalystRole;

GRANT CREATE TABLE ON SCHEMA EXAM_DB.Staging1 TO ROLE ExamDLTRole;
GRANT CREATE TABLE ON SCHEMA EXAM_DB.Staging2 TO ROLE ExamDLTRole;
--- Granting create view on schema mart
GRANT CREATE VIEW ON SCHEMA EXAM_DB.Mart1 TO ROLE ExamDBTRole;
GRANT CREATE VIEW ON SCHEMA EXAM_DB.Mart2 TO ROLE ExamDBTRole;

GRANT CREATE VIEW ON SCHEMA EXAM_DB.WAREHOUSE TO ROLE ExamDBTRole;
<<<<<<< HEAD
=======

>>>>>>> 4c71c1686068e0d9e3726d16f277e4d62ea57fd1
GRANT CREATE VIEW ON SCHEMA EXAM_DB.Mart1 TO ROLE ExamAnalystRole;
GRANT CREATE VIEW ON SCHEMA EXAM_DB.Mart2 TO ROLE ExamAnalystRole;

--- Granting select view on schema mart
GRANT SELECT ON ALL VIEWS IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamDBTRole;
GRANT SELECT ON ALL VIEWS IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamDBTRole;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamDBTRole;

GRANT CREATE TABLE ON SCHEMA EXAM_DB.WAREHOUSE TO ROLE ExamDBTRole;
<<<<<<< HEAD
GRANT SELECT ON ALL VIEWS IN SCHEMA EXAM_DB.Mart TO ROLE ExamAnalystRole;
=======

GRANT SELECT ON ALL VIEWS IN SCHEMA EXAM_DB.Mart1 TO ROLE ExamAnalystRole;
>>>>>>> 4c71c1686068e0d9e3726d16f277e4d62ea57fd1
GRANT SELECT ON ALL VIEWS IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamAnalystRole;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA EXAM_DB.Mart TO ROLE ExamAnalystRole;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA EXAM_DB.Mart2 TO ROLE ExamAnalystRole;
GRANT SELECT ON ALL VIEWS IN SCHEMA EXAM_DB.WAREHOUSE TO ROLE ExamAnalystRole;


--- Granting INSERT, UPDATE, DELETE to DLT Role
GRANT INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDLTRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.STAGING1 TO ROLE ExamDLTRole;

GRANT INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA EXAM_DB.STAGING2 TO ROLE ExamDLTRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.STAGING2 TO ROLE ExamDLTRole;

--- Granting INSERT, UPDATE, DELETE to DBT Role STAGING
GRANT INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDBTRole;

GRANT INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA EXAM_DB.Staging2 TO ROLE ExamDBTRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.Staging1 TO ROLE ExamDBTRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.Staging2 TO ROLE ExamDBTRole;

--- Granting INSERT, UPDATE, DELETE to DBT Role WAREHOUSE
GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.warehouse TO ROLE ExamDBTRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.warehouse TO ROLE ExamDBTRole;

--- Granting INSERT, UPDATE, DELETE to ANALYST Role MART
GRANT INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA EXAM_DB.mart1 TO ROLE ExamAnalystRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.mart1 TO ROLE ExamAnalystRole;

GRANT INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA EXAM_DB.mart2 TO ROLE ExamAnalystRole;

GRANT INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA EXAM_DB.mart2 TO ROLE ExamAnalystRole;

GRANT MODIFY ON DATABASE EXAM_DB TO ROLE ExamDBTRole;
GRANT MODIFY ON SCHEMA WAREHOUSE TO ROLE ExamDBTRole;

-- GRANT TRUNCATE ON ALL TABLES IN SCHEMA Exam_DB.mart TO ROLE ExamDBTRole;
-- GRANT TRUNCATE ON FUTURE TABLES IN SCHEMA Exam_DB.mart TO ROLE ExamDBTRole;


--- Granting roles to users
GRANT ROLE ExamDLTRole TO USER KristoferExamUser;
GRANT ROLE ExamDBTRole TO USER KristoferExamUser;
GRANT ROLE ExamAnalystRole TO USER KristoferExamUser;

GRANT ROLE ExamDLTRole TO USER TimExamUser;
GRANT ROLE ExamDBTRole TO USER TimExamUser;
GRANT ROLE ExamAnalystRole TO USER TimExamUser;

USE DATABASE EXAM_DB;
GRANT CREATE TABLE ON SCHEMA STAGING1 TO ROLE ExamDLTRole;
GRANT CREATE TABLE ON SCHEMA STAGING2 TO ROLE ExamDLTRole;

<<<<<<< HEAD
SHOW GRANTS TO ROLE ExamDBTRole;

SHOW GRANTS TO ROLE ExamAnalystRole;

USE ROLE ORGADMIN;
SHOW ACCOUNTS;
=======
>>>>>>> 4c71c1686068e0d9e3726d16f277e4d62ea57fd1
