BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "courses_tbl" (
	"id"	integer,
	"course_id"	integer NOT NULL UNIQUE,
	"name"	text NOT NULL,
	"description"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "flashcards_tbl" (
	"id"	integer,
	"course_id"	integer NOT NULL,
	"remark"	integer,
	"question"	text NOT NULL,
	"answer"	text NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "remarks_tbl" (
	"id"	INTEGER,
	"description"	text NOT NULL,
	"cource_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
