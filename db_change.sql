USE mydatabase;

create table users
 (
 firstname varchar(50),
 lastname varchar(50),
 email varchar(100),
 password varchar(255),
 primary key(email)
 );
 

drop table REVIEW;
 
 
 CREATE TABLE review (
    review_id int auto_increment,
    email varchar(100),
    language VARCHAR(50),
    input TEXT,
    output TEXT,
    time_and_date DATETIME,
    explanation TEXT,
    accuracy VARCHAR(10),
    raw_response TEXT,
    primary key(review_id)
);

ALTER TABLE REVIEW add constraint foreign key(email) references user(email);

  
  
 