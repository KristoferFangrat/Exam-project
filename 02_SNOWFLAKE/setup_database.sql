'''
   _____      __                 ____        __        __                  
  / ___/___  / /___  ______     / __ \____ _/ /_____ _/ /_  ____ _________ 
  \__ \/ _ \/ __/ / / / __ \   / / / / __ `/ __/ __ `/ __ \/ __ `/ ___/ _ \
 ___/ /  __/ /_/ /_/ / /_/ /  / /_/ / /_/ / /_/ /_/ / /_/ / /_/ (__  )  __/
/____/\___/\__/\__,_/ .___/  /_____/\__,_/\__/\__,_/_.___/\__,_/____/\___/ 
                   /_/                                                     
'''
USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS EXAM_DB;

CREATE WAREHOUSE IF NOT EXISTS exam_wh
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE
COMMENT = 'Warehouse for Exam Project';

USE DATABASE EXAM_DB;

USE WAREHOUSE EXAM_WH;

CREATE SCHEMA IF NOT EXISTS Staging1;
CREATE SCHEMA IF NOT EXISTS Staging2;
CREATE SCHEMA IF NOT EXISTS WAREHOUSE;
CREATE SCHEMA IF NOT EXISTS Mart;


