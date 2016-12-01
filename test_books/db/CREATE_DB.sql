-- Table: authors

-- DROP TABLE authors;

CREATE TABLE authors
(
  saved boolean,
  name character varying(30),
  surname character varying(30),
  id bigserial NOT NULL,
  CONSTRAINT id PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE authors
  OWNER TO postgres;

-- Table: books

-- DROP TABLE books;

CREATE TABLE books
(
  authors_id integer NOT NULL,
  name character varying(100),
  id bigserial NOT NULL,
  CONSTRAINT id_book PRIMARY KEY (id ),
  CONSTRAINT author_id FOREIGN KEY (authors_id)
      REFERENCES authors (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE books
  OWNER TO postgres;
