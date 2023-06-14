### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?

It is an object-relational database system.

- What is the difference between SQL and PostgreSQL?

SQL query language or SQL database? Both use a similar SQL query language

- In `psql`, how do you connect to a database?

/c databasename;

- What is the difference between `HAVING` and `WHERE`?

the HAVING clause is used with aggregates and WHERE is nott

- What is the difference between an `INNER` and `OUTER` join?

an INNER JOIN is the default join and leaves out any rows that do not have a match, OUTER JOIN will include rows with no matching rows

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?

Chooses wich coloumn will include rows without a matching row based on where it is in the query string.

- What is an ORM? What do they do?

Object Relational Management (or mapping). They are a bridge between databases and and object oriented programming

- What are some differences between making HTTP requests using AJAX
  and from the server side using a library like `requests`?

With AJAX, requests are made on the client side within the browser. Server side requests are made on the server and is invisible from the client.

- What is CSRF? What is the purpose of the CSRF token?

CSRF tokens are a way to protect against CSRF attacks.

- What is the purpose of `form.hidden_tag()`?

it is a hidden form field that is used to send a token to prevent CSRF attacks.
