# General simple querys:
* all records in all columns

```
SELECT * 
FROM table;
```

* all records or rows in 1 column or field

```
SELECT col_name1 
FROM table;
```

* all records in 2 columns

```
SELECT col_name1, col_name2 
FROM table;
```

* 10 records in all columns

```
SELECT * 
FROM table LIMIT 10;
```

* random query

```
SELECT 'SQL is cool'
AS result;
```

* non-duplicate values in 1 column

```
SELECT DISTINCT col_name1
FROM table;
```

* non-duplicate values in all columns

```
SELECT DISTINCT *
FROM table;
```

* number of records in table

```
SELECT COUNT(*)
FROM table;
```

* number of  non-missing values in a particular column

```
SELECT COUNT(col_name1)
FROM table;
```

* number of non-duplicate values in 1 column

```
SELECT COUNT(DISTINCT col_name1)
FROM table;
```

## Filtering
The `WHERE` keyword allows you to filter based on both text and numeric values in a table. 

There are a few different comparison operators you can use:

* = equal
* <> not equal
* < less than
* \> greater than
* <= less than or equal to
* \>= greater than or equal to

In addition to those,  the logical operators `AND`, `OR`, `NOT`  allow us to combine comparison operators

>the `WHERE` clause **always** comes after the FROM statement

> use ISO date format for filtering('1974-11-11')

> in PostgreSQL, you must use **single quotes** with `WHERE`

*some examples*

```
SELECT *
FROM table
WHERE col1 > col2;
```

```
SELECT COUNT(DISTINCT col2)
FROM table
WHERE col1 = 'something';
```

* use multiple conditions to select data
```
SELECT *
FROM table
WHERE col1 > col2
AND col1 = 'something';
```

>the column name separately need to be specified for every condition

```
SELECT *
FROM table
WHERE col1 > col2
AND col1 = 'something'
AND col1 <> 'this other thing';
```

>When combining `AND` and `OR`, enclose the individual clauses in parentheses

```
SELECT *
FROM table
WHERE (col1 > col2 OR col3 = 0)
AND (col1 = 'something' OR col1 <> 'this other thing');
```
>The `BETWEEN` keyword provides a useful shorthand for filtering values within a specified range. It is is inclusive, meaning the beginning and end values are included in the results

*some examples*

```
SELECT name
FROM people
WHERE age BETWEEN 20 AND 62
AND nationality = 'Portuguese';
```

>The `IN` operator allows you to specify multiple values in a `WHERE` clause, making it easier and quicker to specify multiple OR conditions

### Count missing/certain values

Missing values are `NULL`. They can be checked using `IS NULL`

```
SELECT COUNT(*)
FROM table
WHERE col1 IS NULL;
```

```
SELECT COUNT(*)
FROM table
WHERE col1 IS NOT NULL;
```

> The `LIKE` operator can be used in a `WHERE` clause to search for a pattern in a column. To accomplish this, you use something called a *wildcard* as a placeholder for some other values. 

1. The `%` wildcard will match zero, one, or many characters in text
2. The `_` wildcard will match a single character.

> `LIKE` is case-sensitive, `ILIKE` is case-insensitive

```
SELECT col
FROM table
WHERE col LIKE '_s%';
```

```
SELECT col
FROM table
WHERE col NOT LIKE '_s%';
```

## Aggregate functions

* such as `MIN`, `MAX`, `AVG`, `SUM`

```
SELECT AVG(col1)
FROM table;
```

* In addition to using aggregate functions, basic arithmetic can be performed  with symbols like `+`, `-`, `*`, and `/`

*SQL assumes that if you divide an integer by an integer, you want to get an integer back. So be careful when dividing, for more precision add decimal places to your numbers

*results  1*

```
SELECT (4 / 3);
```

*results 1.33333333333*

```
SELECT (4.0 / 3.0) AS result;
```

## Aliasing

assign a temporary name to something

```
SELECT MAX(col1) AS max_c1,
       MAX(col2) AS max_c2
FROM table;
```

*examples*

*percentage col1*

```
SELECT COUNT(col1) * 100.0/ COUNT(*) AS percentage_col1
FROM table;
```

## ORDER BY

Keyword used to sort results in ascending or descending order according to the values of one or more columns. By default `ORDER BY` will sort in ascending order

```
SELECT col
FROM table
ORDER BY col;
```

```
SELECT col
FROM table
ORDER BY col DESC;
```

*`ORDER BY` can also be used to sort on multiple columns. It will sort by the first column specified, then sort by the next, then the next, and so on*

## GROUP BY


```
SELECT col1, COUNT(*)
FROM table
GROUP BY col1
ORDER BY count DESC;
```

*Note that `GROUP BY` always goes after the FROM clause. Make sure to always put the `ORDER BY` clause at the end of your query. You can't sort values that you haven't calculated yet*

*SQL will return an error if you try to `SELECT` a field that is not in your `GROUP BY` clause without using it to calculate some kind of value about the entire group*

## HAVING

To filter after an aggregation has taken place, so after a group by call.

Aggregate functions can't be used in `WHERE` clauses.

To filter based on the result of an aggregate function, you need the `HAVING` clause.

```
SELECT col1
FROM table
GROUP BY col1
HAVING count(COL2) > 10;
```