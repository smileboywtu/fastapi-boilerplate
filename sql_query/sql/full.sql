-- name: init_postgres_schema#
create table user(
  username: varchar 64,
  address: varchar 256,
  age: smallint ,
  mobile varchar 16
);

create index username_index on user(username asc );

