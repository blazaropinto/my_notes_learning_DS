# A relational database


A database models real-life entities

Each table only contains data from a single entity type. This reduces redundancy by storing entities only once.

A database can be used to model relationships between entities. You can define exactly how entities relate to each other. 

> "information_schema" is some sort of meta-database that holds information about your current database.
>Once you know the name of a table, you can query its columns by accessing the "columns" table.

*The 'public' schema holds information about user-defined tables and databases.*

*some examples*


```
SELECT table_name 
FROM information_schema.tables
WHERE table_schema = 'public';
```

```
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'nameofthetable' AND table_schema = 'public';
```

* entity-relationship diagram: Squares denote so-called entity types, while circles connected to these denote attributes (or columns).

## Create tables

```
CREATE TABLE table_name (
 column_a data_type,
 column_b data_type,
 column_c data_type
);
```

>Table and columns names, as well as data types, don't need to be surrounded by quotation marks.

>Don't forget commas and final semicolon

### Add columns 

```
ALTER TABLE table_name
ADD COLUMN column_name data_type;
```

### Rename columns:

```
ALTER TABLE table_name
RENAME COLUMN old_name TO new_name;
```

### Delete columns:

```
ALTER TABLE table_name
DROP COLUMN column_name;
```

### Migrate the data into new tables

```
INSERT INTO table1(col1, col2)
SELECT DISTINCT (col1, col2) 
FROM table2
WHERE condition
```

### Add a record to the table

```
INSERT INTO table (col1, col2, col3) 
VALUES 
    ('a', 5, 'b')'
    ('c', 6, 'd');
```

### Table deletion

```
DROP TABLE table_name;
```

## Join tables

```
SELECT *
FROM left_table AS t1
INNER JOIN right_table AS t2
ON t1.id = t2.id;
```

> convention: alias your tables using the first letter of their names

```  
SELECT *
FROM left_table
  INNER JOIN right_table
    ON left_table.id = right_table.id
  INNER JOIN another_table
    ON left_table.id = another_table.id;
```

>When the key field you'd like to join on is the same name in both tables, you can use a `USING` clause (adding parenthesis) instead of the `ON` clause

```
SELECT *
FROM left_table
  INNER JOIN right_table
    USING(id)
```
>self-join

```
SELECT t1.id,
       t1.value AS value1, 
       t2.value AS value2,
       -- 1. calculate growth_perc
       ((t2.value - t1.value)/t1.value * 100.0) AS timechange_perc
FROM table AS t1
  INNER JOIN table AS t2
    ON t1.id = t.id
        AND t1.time = t1.time - xtime;
```

### Update table

```
UPDATE table
SET col1=something,
    col2=anotherthing,
WHERE condition;
```

>UPDATE join:

```
UPDATE table1
SET col1 = table2.col5
FROM table2
WHERE table1.id=table2.id
```

>RETURNING returns the affected columns

```
UPDATE table
SET col1=something
RETURNING col1
```

# Integrity constraints

press the data into a certain form and give consistency, helping to solve a lot of data quality issues

1. **attribute constraints** a certain attribute, represented through a database column, could have the integer *data type*, allowing only for integers to be stored in this column. 
2. **key constraints**. *Primary keys*, for example, uniquely identify each record, or row, of a database table.
3. **referential integrity constraints** enforced through *foreing keys*. In short, they glue different database tables together.

## Type casts
on-the-fly type conversions
>`CAST` function, followed by the column name, the `AS` keyword, and the desired data type

```
SELECT CAST(some_column AS integer)
FROM table;
```

* to change the data type of a column

```
ALTER TABLE table_name
ALTER COLUMN column_name
TYPE varchar(10)
```
* to truncate column values or transform them in any other way, so they fit with the new data type

>you can use the "USING" keyword, and specify a transformation that should happen before the type is altered

* to truncate the values before converting its type

```
ALTER TABLE table_name
ALTER COLUMN column_name
TYPE varchar(x)
USING SUBSTRING(column_name FROM 1 FOR x)
```
*  to disallow NULL values in a column

```
ALTER TABLE table 
ALTER COLUMN col SET NOT NULL;
```

```
CREATE TABLE table_name (
 column_name NOT NULL
);
```

* to add a unique constraint to an existing table

```
ALTER TABLE table_name
ADD CONSTRAINT some_name UNIQUE(column_name);
```

```
CREATE TABLE table_name (
 column_name UNIQUE
);
```

## What is a key?

Typically a database table has an attribute, or a combination of multiple attributes, whose values are unique across the whole table. Such attributes *identify a record uniquely*. Normally, a table, as a whole, only contains unique records, meaning that the combination of all attributes is a key in itself. However, it's not called a key, but a *superkey*, if attributes from that combination can be removed, and the attributes still uniquely identify records.

>simple way of finding out whether a certain column (or a combination) contains only unique values – and thus identifies the records in the table

```
SELECT COUNT(DISTINCT(column_a, column_b, ...))
FROM table;
```

* to set primary key

```
ALTER TABLE table_name
ADD CONSTRAINT some_name PRIMARY KEY (column_name)
```

* to add a SERIAL surrogate key
>special data type serial, which turns the column into an auto-incrementing number.

* to add a surrogate key to an existing table is to concatenate existing columns with the CONCAT() function

```
-- Count the number of distinct rows with columns col1, col2
SELECT COUNT(DISTINCT(col1, col2)) 
FROM cars;

-- Add the id column
ALTER TABLE table
ADD COLUMN id varchar(128);

-- Update id with col1, col2
UPDATE table
SET id = CONCAT(col1, col2);

-- Make id a primary key
ALTER TABLE table
ADD CONSTRAINT id_pk PRIMARY KEY(id);

-- Have a look at the table
SELECT * FROM table;
```
* set foreign keys n-to-1

>designated columns that point to a primary key of another table. 

*restrictions for foreign keys:* 
* the domain and the data type must be the same as one of the primary key. 
* only foreign key values are allowed that exist as values in the primary key of the referenced table. This is the actual foreign key constraint, also called "*referential integrity*".
* is not necessarily an actual key, because duplicates and "NULL" values are allowed.

>**Referential integrity** states that a record referencing another record in another table must always refer to an existing record.

*Tell the database system what should happen if an entry in the referenced table is deleted. By default, the `ON DELETE NO ACTION` keyword is automatically appended to a foreign key definition. Another options: `ON DELETE CASCADE`, 'ON DELETE SET NULL`, `ON DELETE SET DEFAULT*

```
ALTER TABLE a 
ADD CONSTRAINT a_fkey FOREIGN KEY (b_id) REFERENCES b (id);
```

> **naming convention**  a foreign key referencing another primary key with name id is named x_id, where x is the name of the referencing table in the singular form.

* set foreign keys n-to-m
>create a table with foreig keys for every conected table + additional atributes with no primary key

```
-- Add a professor_id column
ALTER TABLE affiliations
ADD COLUMN professor_id integer REFERENCES professors (id);

-- Rename the organization column to organization_id
ALTER TABLE affiliations
RENAME organization TO organization_id;

-- Add a foreign key on organization_id
ALTER TABLE affiliations
ADD CONSTRAINT affiliations_organization_fkey FOREIGN KEY (organization_id) REFERENCES organizations (id);
```

* to update columns of a table based on values in another table:

```
UPDATE table_a
SET column_to_update = table_b.column_to_update_from
FROM table_b
WHERE condition1 AND condition2 AND ...;
```

* Altering a key constraint doesn't work with `ALTER COLUMN`. Instead, you have to `DROP` the key constraint and then `ADD` a new one with a different `ON DELETE` behavior.

>For deleting constraints, though, you need to know their name. This information is also stored in `information_schema`

```
-- Identify the correct constraint name
SELECT constraint_name, table_name, constraint_type
FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY';
```

* another kind of constraint is CHECK

```
CREATE TABLE table(
    col1 smallint CHECK(col1<10)
);
```

# CASE THEN WHEN END

to categorize groups of values..

```
SELECT col1, col2,
    CASE WHEN condition_for_col3 THEN 'something'
        WHEN condition_for_col3 THEN 'anotherthing'
        ELSE 'somethingelse' END
        AS types
FROM table;
```

##  INTO table

```
SELECT col1, col2,
    CASE WHEN condition_for_col3 THEN 'something'
        WHEN condition_for_col3 THEN 'anotherthing'
        ELSE 'somethingelse' END
        AS types
INTO tab2
FROM table;

SELECT*
FROM tab2
```