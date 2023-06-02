CREATE TABLE movie
(
  id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  price INT NOT NULL,
  description VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE auditorium
(
  id INT NOT NULL,
  capacity INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE customer
(
  email VARCHAR(100) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone INT NOT NULL,
  PRIMARY KEY (email)
);

CREATE TABLE viewing
(
  id INT NOT NULL,
  date_time DATETIME NOT NULL,
  auditorium_id INT NOT NULL,
  movie_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (auditorium_id) REFERENCES auditorium(id),
  FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE TABLE ticket
(
  id INTEGER PRIMARY KEY NOT NULL,
  ticket_amount INT NOT NULL,
  viewing_id INT NOT NULL,
  email VARCHAR(100) NOT NULL,
  FOREIGN KEY (viewing_id) REFERENCES viewing(id),
  FOREIGN KEY (email) REFERENCES customer(email)
);

INSERT INTO movie VALUES
(1, "Star Wars", 150, "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader."),
(2, "Spider-Man: No Way Home", 260, "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man."),
(3, "The Godfather", 100, "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son."),
(4, "The Lion King", 75, "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."),
(5, "The Shawshank Redemption", 190, "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.");

INSERT INTO auditorium VALUES 
(1, 100),
(2, 200),
(3, 300);

INSERT INTO viewing VALUES
(1, '2022-05-05 15:30:00', 1, 4),
(2, '2022-05-05 15:30:00', 2, 1),
(3, '2022-05-05 16:00:00', 3, 1),
(4, '2022-05-05 20:00:00', 1, 1),
(5, '2022-05-05 21:30:00', 3, 5),
(6, '2022-05-06 15:30:00', 2, 4),
(7, '2022-05-06 17:00:00', 1, 3),
(8, '2022-05-06 19:30:00', 3, 2);

INSERT INTO customer VALUES
("elizke2@gmail.com", "Elizabeth", "Keller", 95642817),
("grady2009@yahoo.com", "Eric", "Kromer", 48240065),
("seidman1997@gmail.com", "Terrie", "Seidman", 90215695),
("maydun123@gmail.com", "May", "Dunn", 93753800),
("oivind.o@gmail.com", "Øivind", "Wisløff", 92356752);