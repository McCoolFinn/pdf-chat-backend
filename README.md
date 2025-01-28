# PDF-Chat Backend Server

This is a server for hosting a document store + chat application. It stems from a prompt challenge for an interview.

*Dependencies: quart, asyncpg

## Running the server:
### Install SQL schema
`./schema.sql` includes the necessary SQL schema for the data. You can import that into a database of your choosing (pgAdmin, console, etc). Then just update:

    postgresql://postgres:PASSWORD@localhost:5432/pdf_chat

To reflect your database connection settings.

### Run the Server
Run the following commands from the root:

    (Optional)
    python -m venv venv
    ./venv/Scripts/activate
    (Required)
    pip install quart asyncpg
    quart --app backend.pdf-chat run
