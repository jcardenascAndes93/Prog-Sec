# create databases
CREATE DATABASE IF NOT EXISTS `test`;

# create user and grant rights
CREATE USER 'test' IDENTIFIED BY 'test';
GRANT USAGE ON *.* TO `test`@`%`;
GRANT ALL PRIVILEGES ON `test`.* TO `test`@`%`;
