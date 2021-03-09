DROP DATABASE IF EXISTS sola;

create DATABASE sola collate utf8_unicode_ci;
USE sola;
DROP TABLE IF EXISTS EM_company;
CREATE TABLE EM_company
(
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    name                  VARCHAR(128) NOT NULL,
    furigana              VARCHAR(128),
    zip                   CHAR(10),
    address               VARCHAR(256),
    date_of_establishment DATE,
    number_o_employees    VARCHAR(64),
    legal_entity_number   VARCHAR(64),
    phone_number          VARCHAR(20),
    fax_number            VARCHAR(20),
    coords                VARCHAR(128),
    accept_range          FLOAT                 DEFAULT 0.2,
    locked                TINYINT(1)   NOT NULL DEFAULT 0,
    modified              TIMESTAMP,
    user_modified         INT,
    created_user          INT,
    created_time          TIMESTAMP
);
CREATE INDEX EM_company_index1 ON EM_company (name);
CREATE INDEX EM_company_index2 ON EM_company (locked);

DROP TABLE IF EXISTS EM_company_attachment;
CREATE TABLE EM_company_attachment
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(256) NOT NULL,
    path          VARCHAR(256) NOT NULL,
    priority      INT          NOT NULL DEFAULT 0,
    locked        TINYINT(1)   NOT NULL DEFAULT 0,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP
);

DROP TABLE IF EXISTS EM_department;
CREATE TABLE EM_department
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(256) NOT NULL,
    description   VARCHAR(512),
    priority      INT                   DEFAULT 0,
    locked        TINYINT(1)   NOT NULL DEFAULT 0,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP
);
CREATE INDEX EM_department_index1 ON EM_department (name);
CREATE INDEX EM_department_index2 ON EM_department (locked);

DROP TABLE IF EXISTS EM_jobtitle;
CREATE TABLE EM_jobtitle
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(256) NOT NULL,
    description   VARCHAR(512),
    priority      INT                   DEFAULT 0,
    locked        TINYINT(1)   NOT NULL DEFAULT 0,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP

);
CREATE INDEX EM_jobtitle_index1 ON EM_jobtitle (locked);

DROP TABLE IF EXISTS EM_user;
CREATE TABLE EM_user
(
    id                         INT AUTO_INCREMENT PRIMARY KEY,
    username                   CHAR(64)   NOT NULL,
    fullname                   CHAR(64)   NOT NULL,
    locked                     TINYINT(1) NOT NULL DEFAULT 0,
    gender                     CHAR       NOT NULL,
    password                   CHAR(64)   NOT NULL,
    role_id                    INT        NOT NULL,
    furigana                   VARCHAR(128),
    birthday                   DATE,
    zip                        CHAR(10)   null,
    address                    VARCHAR(512),
    phone                      VARCHAR(64),
    email                      VARCHAR(64),
    bank_name                  VARCHAR(64),
    branch_name                VARCHAR(64),
    account_type               VARCHAR(32),
    account_number             VARCHAR(64),
    my_number                  VARCHAR(64),
    pension_number             VARCHAR(64),
    registration_date          DATE,
    insurance_insured_person   VARCHAR(64),
    activeor_retirement_status TINYINT(1),
    department_id              INT        NOT NULL,
    base_salary                FLOAT,
    commute_allowance          FLOAT,
    modified                   TIMESTAMP,
    user_modified              INT,
    created_user               INT,
    created_time               TIMESTAMP
);
CREATE INDEX EM_user_index1 ON EM_user (locked);
CREATE INDEX EM_user_index2 ON EM_user (role_id);
CREATE INDEX EM_user_index3 ON EM_user (department_id);

DROP TABLE IF EXISTS EM_job;
CREATE TABLE EM_job
(
    id             INT AUTO_INCREMENT PRIMARY KEY,
    start_date     timestamp,
    end_date       timestamp,
    owner_name     VARCHAR(64),
    owner_phone    VARCHAR(64),
    e_in_charge    INT,
    postal_code    VARCHAR(12),
    address        VARCHAR(128),
    description    VARCHAR(512),
    street_id      INT,
    district_id    INT,
    province_id    INT,
    worker_count   INT,
    required_stuff VARCHAR(1024),
    leader_id      INT,
    name           VARCHAR(128),
    modified       TIMESTAMP,
    user_modified  INT,
    created_user   INT,
    created_time   TIMESTAMP
);
CREATE INDEX EM_job_index1 ON EM_job (start_date);
CREATE INDEX EM_job_index2 ON EM_job (end_date);
CREATE INDEX EM_job_index3 ON EM_job (leader_id);

DROP TABLE IF EXISTS EM_user_job;
CREATE TABLE EM_user_job
(
    job_id  INT NOT NULL,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    status  INT NOT NULL
);
CREATE INDEX EM_user_job_index1 ON EM_user_job (job_id);
CREATE INDEX EM_user_job_index2 ON EM_user_job (user_id);
CREATE INDEX EM_user_job_index3 ON EM_user_job (role_id);
CREATE INDEX EM_user_job_index4 ON EM_user_job (status);

DROP TABLE IF EXISTS EM_role;
CREATE TABLE EM_role
(
    id       INT AUTO_INCREMENT PRIMARY KEY,
    slug     CHAR(32) NOT NULL,
    name     VARCHAR(64),
    priority TINYINT(2)
);

INSERT INTO EM_role(id, slug, name, priority)
VALUES (1, 'admin', 'Administrator', 1);
INSERT INTO EM_role(id, slug, name, priority)
VALUES (2, 'master', 'Master', 2);
INSERT INTO EM_role(id, slug, name, priority)
VALUES (3, 'manager', 'Manager', 3);
INSERT INTO EM_role(id, slug, name, priority)
VALUES (4, 'leader', 'Leader', 4);
INSERT INTO EM_role(id, slug, name, priority)
VALUES (5, 'worker', 'Worker', 5);
INSERT INTO EM_role(id, slug, name, priority)
VALUES (6, 'accounttant', 'Accounttant', 6);
CREATE INDEX EM_role_index1 ON EM_role (slug);


DROP TABLE IF EXISTS EM_relationship;
CREATE TABLE EM_relationship
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(128),
    locked        TINYINT(1) NOT NULL DEFAULT 0,
    priority      INT,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP
);

DROP TABLE IF EXISTS EM_dependent;
CREATE TABLE EM_dependent
(
    id              INT AUTO_INCREMENT PRIMARY KEY,
    employee_id     INT         NOT NULL,
    name            VARCHAR(64) NOT NULL,
    furigana        VARCHAR(64),
    birthday        DATE,
    is_dependent    TINYINT(1)           DEFAULT 0,
    relationship_id INT         NOT NULL,
    locked          TINYINT(1)  NOT NULL DEFAULT 0,
    modified        TIMESTAMP,
    user_modified   INT,
    created_user    INT,
    created_time    TIMESTAMP
);
CREATE INDEX EM_dependent_index1 ON EM_dependent (employee_id);


DROP TABLE IF EXISTS EM_expense_document;
CREATE TABLE EM_expense_document
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    employee_id   INT          NOT NULL,
    path          VARCHAR(256) NOT NULL,
    content       TEXT,
    locked        TINYINT(1) DEFAULT 0,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP
);
CREATE INDEX EM_expense_document_index1 ON EM_expense_document (employee_id);

DROP TABLE IF EXISTS EM_time_record;
CREATE TABLE EM_time_record
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT        NOT NULL,
    time_in       TIMESTAMP,
    time_out      TIMESTAMP,
    duration      INT,
    overtime      INT,
    coord_in      VARCHAR(64),
    coord_out     VARCHAR(64),
    distance_in   FLOAT,
    distance_out  FLOAT,
    approved      TINYINT(2)          DEFAULT 0,
    locked        TINYINT(1) NOT NULL DEFAULT 0,
    created_time  TIMESTAMP  NOT NULL,
    modified      TIMESTAMP  NOT NULL,
    created_user  INT        NOT NULL,
    user_modified INT        NOT NULL
);
CREATE INDEX EM_time_record_index1 ON EM_time_record (user_id);
CREATE INDEX EM_time_record_index2 ON EM_time_record (locked);
CREATE INDEX EM_time_record_index3 ON EM_time_record (approved);
CREATE INDEX EM_time_record_index4 ON EM_time_record (time_in);

DROP TABLE IF EXISTS EM_workdays;
CREATE TABLE EM_workdays
(
    id               INT AUTO_INCREMENT PRIMARY KEY,
    month            INT        NOT NULL,
    year             INT        NOT NULL,
    workdays         FLOAT,
    weekend_days     FLOAT,
    national_holiday FLOAT,
    locked           TINYINT(1) NOT NULL DEFAULT 0,
    modified         TIMESTAMP,
    user_modified    INT,
    created_user     INT,
    created_time     TIMESTAMP
);
CREATE INDEX EM_workdays_index1 ON EM_workdays (month);
CREATE INDEX EM_workdays_index2 ON EM_workdays (year);


DROP TABLE IF EXISTS EM_notification;
CREATE TABLE EM_notification
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    content       VARCHAR(1024),
    locked        TINYINT(1) NOT NULL DEFAULT 0,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP
);


DROP TABLE IF EXISTS EM_holiday;
CREATE TABLE EM_holiday
(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT        NOT NULL,
    reason        VARCHAR(256),
    date          DATE       NOT NULL,
    locked        TINYINT(1) NOT NULL DEFAULT 0,
    modified      TIMESTAMP,
    user_modified INT,
    created_user  INT,
    created_time  TIMESTAMP,
    approved      TINYINT,
    approval_user INT,
    approval_time TIMESTAMP
);

CREATE INDEX EM_holiday_index1 ON EM_holiday (user_id);
CREATE INDEX EM_holiday_index2 ON EM_holiday (approved);
CREATE INDEX EM_holiday_index3 ON EM_holiday (locked);


