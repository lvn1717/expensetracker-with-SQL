create database expense_tracker;
use expense_tracker;

create table expenses(
id int auto_increment primary key,
date date,
description varchar(255),
amount decimal(10,2),
category varchar(100)
);
