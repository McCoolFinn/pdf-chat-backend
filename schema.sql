CREATE TYPE gender AS ENUM ('male', 'female', 'non-binary');
CREATE TYPE filetype AS ENUM ('pdf');
CREATE TYPE conversation AS ENUM ('direct', 'group');

CREATE TABLE IF NOT EXISTS "users" (
	"id" serial NOT NULL UNIQUE,
	"username" varchar(32) NOT NULL UNIQUE,
	"display_name" varchar(64) NOT NULL,
	"email" varchar(64) NOT NULL UNIQUE,
	"password" character(64) NOT NULL,
	"gender" gender NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "documents" (
	"id" serial NOT NULL UNIQUE,
	"user_id" bigint NOT NULL,
	"filename" varchar(128) NOT NULL,
	"filetype" filetype NOT NULL,
	"data" bytea NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "documents_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("id")
);

CREATE TABLE IF NOT EXISTS "conversations" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(64),
	"type" conversation NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "participants" (
	"conversation_id" bigint NOT NULL,
	"user_id" bigint NOT NULL,	
	CONSTRAINT "participants_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("id"),
	CONSTRAINT "participants_fk2" FOREIGN KEY ("conversation_id") REFERENCES "conversations"("id")
);

CREATE TABLE IF NOT EXISTS "messages" (
	"id" serial NOT NULL UNIQUE,
	"sender_id" bigint,
	"conversation_id" bigint NOT NULL,
	"content" text NOT NULL,
	"timestamp" timestamp with time zone NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "messages_fk1" FOREIGN KEY ("sender_id") REFERENCES "users"("id"),
	CONSTRAINT "messages_fk2" FOREIGN KEY ("conversation_id") REFERENCES "conversations"("id")
);

CREATE TABLE IF NOT EXISTS "auths" (
	"key" character(64) NOT NULL,
	"user_id" integer NOT NULL,
	PRIMARY KEY ("key"),
	CONSTRAINT "auths_fk1" FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);