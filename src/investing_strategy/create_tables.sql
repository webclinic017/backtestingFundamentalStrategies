create database bolsa;
use bolsa;
create table calendario(
 id int PRIMARY KEY,
 fecha datetime,
 zone varchar(100),
 currency varchar(100),
 importance varchar(100),
 event varchar(100),
 actual varchar(100),
 forecast varchar(100),
 previus varchar(100)

);
