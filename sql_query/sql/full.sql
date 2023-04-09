-- name: init_postgres_schema#
CREATE TABLE IF NOT EXISTS Company(
  company_name varchar(64),
  company_address varchar(256)
);

create index if not exists  companyname_index on Company(company_name asc );

