-- name: get_all_users
-- Get all user list
-- record_class: User
select id, username, address, age, mobile from user;

-- name: get_user_by_id
-- Get user detail
-- record_class: User
select id, username, address, age, mobile from user where id = :id;

-- name: add_new_user
-- Add new user
-- record_class: User