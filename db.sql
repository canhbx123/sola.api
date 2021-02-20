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
    memo1                 VARCHAR(256),
    memo2                 VARCHAR(256),
    memo3                 VARCHAR(256),
    locked                TINYINT(1)   NOT NULL,
    modified              TIMESTAMP,
    user_modified         INT,
    created_user          INT,
    created_time          TIMESTAMP
);
CREATE INDEX EM_company_index1 ON EM_company (name);
CREATE INDEX EM_company_index2 ON EM_company (locked);


CREATE TABLE EM_department
(
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(256) NOT NULL,
    locked      tinyINT(1)   NOT NULL,
    description VARCHAR(512),
    modified    timestamp    NOT NULL
);
CREATE INDEX EM_department_index1 ON EM_department (name);
CREATE INDEX EM_department_index2 ON EM_department (locked);


DROP TABLE IF EXISTS EM_user;
CREATE TABLE EM_user
(
    id                         INT AUTO_INCREMENT PRIMARY KEY,
    username                   CHAR(64)   NOT NULL,
    fullname                   CHAR(64)   NOT NULL,
    locked                     TINYINT(1) NOT NULL,
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
    id   INT AUTO_INCREMENT PRIMARY KEY,
    slug CHAR(32) NOT NULL,
    name VARCHAR(64)
);

INSERT INTO EM_role(id, slug, name)
VALUES (1, 'admin', 'Administrator');
INSERT INTO EM_role(id, slug, name)
VALUES (2, 'master', 'Master');
INSERT INTO EM_role(id, slug, name)
VALUES (3, 'manager', 'Manager');
INSERT INTO EM_role(id, slug, name)
VALUES (4, 'leader', 'Leader');
INSERT INTO EM_role(id, slug, name)
VALUES (5, 'worker', 'Worker');
INSERT INTO EM_role(id, slug, name)
VALUES (6, 'accounttant', 'Accounttant');
CREATE INDEX EM_role_index1 ON EM_role (slug);


DROP TABLE IF EXISTS EM_relationship;
CREATE TABLE EM_relationship
(
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(128),
    locked   TINYINT(1),
    priority TINYINT(3)
);

DROP TABLE IF EXISTS EM_dependent;
CREATE TABLE EM_dependent
(
    id              INT AUTO_INCREMENT PRIMARY KEY,
    employee_id     INT         NOT NULL,
    name            VARCHAR(64) NOT NULL,
    furigana        VARCHAR(64),
    birthday        DATE,
    relationship_id INT         NOT NULL,
    is_dependent    TINYINT(1)  NOT NULL,
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
    user_id       INT NOT NULL,
    time_in       TIMESTAMP,
    time_out      TIMESTAMP,
    lat           FLOAT,
    lon           FLOAT,
    status        TINYINT DEFAULT 0,
    created_time  TIMESTAMP,
    modified      TIMESTAMP,
    user_modified INT
);
CREATE INDEX EM_time_record_index1 ON EM_time_record (user_id);

