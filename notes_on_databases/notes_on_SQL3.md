# SQL table joins

## INNER JOIN

Also denoted as just JOIN in SQL.

> table order doesn't matter for this type of join

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
INNER JOIN table2 AS t2
ON t1.id = t2.id;
```

### Self-join

A special case of an INNER JOIN. 

```
SELECT t1.col1 AS c1, t1.col1 AS c2
FROM table1 AS t1
INNER JOIN table1 AS t2
ON t1.id = t2.id
AND t1.col2 <> t2.col2;
```

## OUTER JOINs

### LEFT JOIN (or LEFT OUTER JOIN)

keeps all reconds from left table adding features from second table where pertinent

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
LEFT JOIN table2 AS t2
ON t1.id = t2.id;
```
#### Clarifying WHERE null


rows found in the left table a and not found in the right table.

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
LEFT JOIN table2 AS t2
ON t1.id = t2.id
WHERE t2.col2 IS NULL;
```


### RIGHT JOIN (or RIGHT OUTER JOIN)

the opposite

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
RIGHT JOIN table2 AS t2
ON t1.id = t2.id;
```

#### Clarifying WHERE null

rows found in the right table a and not found in left table.

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
RIGHT JOIN table2 AS t2
ON t1.id = t2.id
WHERE t1.col2 IS NULL;
```


### FULL JOIN (or FULL OUTER JOIN)

both joins above together

>order does not matter

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
FULL JOIN table2 AS t2
ON t1.id = t2.id;
```

#### Clarifying WHERE null

to get rows that are not found in either table (so this is the exact opposite of an inner join).

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
FULL JOIN table2 AS t2
ON t1.id = t2.id
WHERE t1.col2 IS NULL OR t2.col2 IS NULL;
```

## CROSS JOINs 

To create all possible combinations between two tables. 

```
SELECT t1.col1, t2.col1
FROM table1 AS t1
CROSS JOIN table2 AS t2;
```

> Self-joins, semi-joins, and anti-joins don't have built-in SQL syntax.

## Semi-joins 

to filter your first table based on conditions set on a second table, you should use a semi-join to accomplish your task.

```
SELECT col1, col2
FROM table1
WHERE col2 IN
    (SELECT colx
    FROM table2
    WHERE condition);
```

## Anti-joins. 

to filter your first table based on conditions NOT being met on a second table, you should use an anti-join. 

>Anti-joins are particularly useful in diagnosing problems with other joins in terms of getting fewer or more records than you expected.

```
SELECT col1, col2
FROM table1
WHERE col2 NOT IN
    (SELECT colx
    FROM table2
    WHERE condition);
```

# Set Theory Clauses

## UNION 

includes every record in both tables but DOES NOT double count those that are in both tables 

is used to combine the results set of two or more select statements and serves to directly concatenate two results together (essentially just pasting the results of two select statements right on top of each other)

```
SELECT col1 AS t1_col1 
FROM table1 
UNION 
SELECT col1 AS t2_col1
FROM table2;
```

## UNION ALL 

DOES replicate those that are in both tables.

## INTERSECT 

gives only those records found in both of the two tables. 

```
SELECT col1 AS t1_col1 
FROM table1 
INTERSECT 
SELECT col1 AS t2_col1
FROM table2; 
```

## EXCEPT 

gives only those records in one table BUT NOT the other.

```
SELECT col1 AS t1_col1 
FROM table1 
EXCEPT 
SELECT col1 AS t2_col1
FROM table2 ;
```

# Subqueries

inside of a:

## WHERE clause

The most frequent type.

```
SELECT col1, col2
FROM table1
WHERE condition
AND col2 <
(SELECT AVG(col2)
FROM table1);
```

## SELECT clause
 
## FROM clause
 
## ON statement of a join 


# Conditional expresions and procedures

## CASE

to only execute SQL code when other conditions are met, like for instance "a substitute for a column call"

### "general" CASE

```
CASE
    WHEN condition1_expressiontovalue1 THEN result1
    WHEN condition2_expressiontovalue2 THEN result2
    ELSE result3
END
```

```
SELECT col1,
    CASE
    WHEN condition1_expressiontovalue1 THEN result1
    WHEN condition2_expressiontovalue2 THEN result2
    ELSE result3
    END AS new_col
FROM table
```

### CASE expression

first evaluates an expression then compares the result with each value in the WHEN clauses sequentially

```
CASE expression
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE result3
END
```
```
SELECT col1,
    CASE expression
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE result3
    END AS new_col
FROM table
```

## COALESCE

returns the first non null argument

    > returns null if all arguments are null)

* common use: replace null values with 0 (to perform operations with some column)

'''
SELECT col1, COALESCE(col2, 0)
FROM table
```

## CAST

convert to another data type if possible

'''
CAST('1' as integer)
```

```
SELECT CAST(col1 AS TIMESTAMP)
FROM table
```

```
SELECT CAST(col1 AS VARCHAR)
FROM table
```

## NULLIF

function that takes 2 inputs and return NULL if both are equal, otherwise returs the first

>useful to make sure somethig is not 0 whe performing a division, if is 0 we get null instead of error

```
SELECT col1 / NULLIF(col2, 0)
FROM TABLE
```

## Views

to store an often used query, create a "virtual table" (this table is not stored, the query is)

```
CREATE VIEW view_name AS
SELECT *
FROM table;

SELECT * FROM view_name;
```

to chage, rename or detete, use:

`CREATE OR REPLACE VIEW` 
`ALTER VIEW view_name RENAME TO view_name2`
`DROP VIEW IF EXISTS`

# Other common funtions

## SHOW

### SHOW ALL

### SHOW TIMEZONE

## Current time information

### SELECT NOW() 
gives the currrent timestamp

### SELECT TIMEOFDAY()
returns a string

### SELECT CURRENT_TIME

### SELECT CURRENT_DATE


## EXTRACT()

obtain a sub component of a date value 'EXTRACT(YEAR FROM col)

### year 

### month 

### day 

### week 

### quarter

## AGE()

calculates and returns the current age given a timestamp 'AGE(col) 

## TO_CHAR()

convert data types to text `TO_CHAR(col,'%')

> useful for timestamp formatting

## Mathematical functions and operators

### /,*,+,-

### % , ^

remainder and exponential

### ROUND

'ROUND(col1,2)`

## String functions and operators

### LENGTH

### CHAR_LENGTH

### LOWER or UPPER

### || 

'col1 || col2` to concatenate strings 

### LEFT

'LEFT(col1,1)` returns the first char of string in col1