There are several great tools that we can use in Python when working with databases.One of those is:

# SQLAlchemy 

SQLAlchemy will allow us to generate SQL queries by writing Python code.

SQLAlchemy has two main components:
1. focused around the relational model of the database: the "core".
2. focused around data models and classes that you as a programmer create: the Object Relational Model or ORM part

It provides a way to operate across all of these database types in a consistent manner.

> There are many different types of databases, each with its own quirks and  capabilities, such as SQLite, PostgreSQL, MySQL, Microsoft SQL Server, and Oracle.

# Connecting to a database

An engine provides "a way to talk to the databese", an interface.

```
from sqlalchemy import  create_engine 
# then use the function and supply it with a connection str with the required details
engine = create_engine('sqlite:///xx.sqlite')
# use the connect method on the engine
connection = engine.connect()
```

> The string provided, in the simplest form, tell us what kind of database we are talking to (database driver) and how we should access it (filename)

> Common drivers for databases:
* `psycopg2` for PostgreSQL
* `pymysql` for MySQL

#### To ask what tables are contained in the database

```
engine.table_names()
```

#### Reflection

To read the database and build a Table object that we can use in our code.

> Reflection is the process of reading the database and building the metadata based on that information. It's the opposite of creating a Table by hand and is very useful for working with existing databases.

```
from sqlalchemy import MetaData, Table 
metadata = MetaData() 
xx = Table('xx', metadata, autoload=True, autoload_with=engine) 
#the function repr allow us to see the details
print(repr(xx))
```

> For any Python object, `repr()` returns a text representation of that object.

*  examining the column names: `tablename.columns.keys()`

Information about the table objects are stored in the `metadata.tables` dictionary

* getting the metadata of your table with `metadata.tables['tablename']`

#### general queries

```
from sqlalchemy import create_engine
engine = create_engine('sqlite:///xx.sqlite')
connection = engine.connect()
query = 'SELECT * FROM xx_table'
result_proxy = connection.execute(query)
results = result_proxy.fetchall()
```

* The object that the execute method gave us is called **ResultProxy** 

* When we use a fetch method, such as fetchall, on the ResultProxy, we get a **ResultSet** that contains the actual data we asked for in the query. 

> This separation allows us to fetch as much  data as we need. 

***SQL statements*** can be written as a **strings**; but SQLAlchemy  allows us to assemble these  statements **in a Pythonic way**(code that adheres to the idioms of Python's common guidelines and expresses its intent in a highly readable way). SQLAlchemy also hides the difference between database types so we can focus on the data.

* the function `select()` requires a **list**

```
from sqlalchemy import Table, MetaData
metadata = MetaData() 
xx = Table('xx', metadata, autoload=True,autoload_with=engine) 
stmt = select([census])
results = connection.execute(stmt).fetchall()
```

* `fetchmany(size=n)` takes the number of record as an argument

* the result set is like a **list**, so the first row of the queried data can be accesed through `result_set[0]`

*  In general, connection strings have the form "dialect+driver://username:password@host:port/database"

#### filtering

```
stmt = select([xx])
stmt = stmt.where(xx.columns.col1 == 'something')
results = connection.execute(stmt).fetchall()
for result in results:
    print(result.col1, result.col2)
```

> the monst common expressions:
* `.where()`
* `.order_by()` to order in ascending order.
* `desc()` is used inside `order by()`, with the column as argument. It has to be imported from sqlalchemy.
* the `func` module has to be imported to use `func.sum()` or `func.count()` (then use `scalar()` instead of `.fetchall()` to obtain the single number)
* `group_by()` requires the use of an agg function, so the `func` module needs to be imported as well.
* `.distinct()`

> see [the documentation] for a full list of expressions.

> if you are only interested in manipulating one record at a time, you can iterate over the ResultProxy directly

> When you use an agg function such as sum or count, the column name that represents the function in our results is set to a placeholder. The  `label()` method can be used on a function to give the output column a specific name.

> the results can be easily used in pandas

```
# Import pyplot as plt from matplotlib
import matplotlib.pyplot as plt
import pandas as pd
# Create a DataFrame from the results: df
df = pd.DataFrame(results)
# Set Column names
df.columns = results[0].keys()
# Print the DataFrame
print(df.head())
# Plot the DataFrame
df.plot.bar()
plt.show()
```

#### math operations

* `+`
* `-`
* `*`
* `/`
* `%`

> They behave differently when used with non-numeric column types.

#### cast

to treat data differently based on a condition.  The `case()` expression accepts a list of conditions to match and the column to return if the condition matches, followed by an `else_` if none of the conditions match. 


```
from sqlalchemy import case
stmt = select([        
    func.sum(            
        case([                
            (xx.columns.col1 == 'something',                  
            xx.columns.col2)            
            ], else_=0))])
results = connection.execute(stmt).fetchall()
print(results)
```

#### cast

Converts data to another type

```
from sqlalchemy import case, cast, Float
stmt = select([        
    (func.sum(            
        case([                
            (xx.columns.col1 == 'something',                  
            xx.columns.col2)            
            ], else_=0)) /         
        cast(func.sum(xx.columns.col2),               
            Float) * 100).label('percent')])
results = connection.execute(stmt).fetchall()
print(results)
```


#### Automatic joins

They use predefined relationship between tables. SQLAlchemy ***automatically*** adds the right join clause because it is predefined in the database.

```
# Build a statement to join both tables: 
stmt = select([xx.columns.col1, table2.columns.col2])
# Execute the statement and get the first result: 
result = connection.execute(stmt).first()
```

#### Join

* The `.join()` takes the table object you want to join in as the first argument and a condition that indicates how the tables are related to the second argument. 
* Finally, you use the `.select_from()` method on the select statement to wrap the join clause (it is passed as the argument)

```
# Build a statement to select the ALL THE COLUMNS in both tables: 
stmt = select([xx, table2])
# Add a select_from clause that wraps a join for the both tables where col1 from xx  and col2 from table2  match
stmt_join = stmt.select_from(
    xx.join(table2, xx.columns.col1 == table2.columns.col2))
# Execute the statement and get the first result: result
result = connection.execute(stmt_join).first()
```

#### self-referential or hierarchical tables

The `.alias()` method, which creates a copy of a table, helps accomplish this task. Because it's the same table, you only need a where clause to specify the join condition.

```
# Make an alias of the employees table: managers
copy_xx = xx.alias()
# Build a query to select names of managers and their employees: stmt
stmt = select(
    [copy_xx.columns.col1.label('co_xx'),
     xx.columns.col1.label('xx')]
)
# Match co_id from copy_xx id with id from xx: 
stmt_matched = stmt.where(copy_xx.columns.co_id == xx.columns.id)
# Order the statement by co_xx: 
stmt_ordered = stmt_matched.order_by(copy_xx.columns.col1)
# Execute statement: 
results = connection.execute(stmt_ordered).fetchall()
```

#### Dealing with large ResultSets

The `fetchmany()` method  allows us to retrieve results so many at a time (in blocks of rows), we can use the method in a loop. 
* When there are no more records, fetchmany will return an empty list, meaning you have processed all the results of the query. 
* Because the result proxy does not know when we are done calling fetchmany, we must call the `.close()`  method on the result proxy when we are done.

```
# Start a while loop checking for more results
while more_results:
    # Fetch the first 50 results from the ResultProxy: partial_results
    partial_results = results_proxy.fetchmany(50)
    # if empty list, set more_results to False
    if partial_results == []:
        more_results = False
    # Loop over the fetched records and increment the count of col1 in the previously inicialised dictionary:
    for row in partial_results:
        if row.col1 in dictionary:
            dictionary[row.col1] += 1
        else:
            dictionary[row.col1] = 1

# Close the ResultProxy, and thus the connection
results_proxy.close()
```

#### Create databases

often requires the use of a command line tool or management application

> With SQLite, if you supply a filename that does not exist to the create_engine method, it will create that file which creates the database.

> Unlike most other SQL databases, SQLite does not have a separate server process. SQLite reads and writes directly to ordinary disk files. A complete SQL database with multiple tables, indices, triggers, and views, is contained in a single disk file

> The SQLite files are generally stored on the internal storage under `/data/data/<packageName>/databases`. However, there are no restrictions on creating databases elsewhere.

#### build a table

first, import everything you need (Table, Column and all data types)

> use the Table object to create a table in the previously created metadata with a few columns. 

> The Table object is therefore used both to reflect an *existing* table and to create a *new* one (using the `autoload` and `autoload_with` parameters or the `Column` object respectively)

> After defining the table, you can create the table in the database by using the .`create_all()` method on metadata and supplying the engine as the only parameter.

```
# Import Table, Column, String, Integer, Float, Boolean from sqlalchemy
from sqlalchemy import Table, Column, String, Integer, Float, Boolean 
# Define a new table with a name, count, amount, and valid column: data
data = Table('xx', metadata,
             Column('c1', String(255), unique=True),
             Column('c2', Integer(), default=1),
             Column('c3', Float()),
             Column('c4', Boolean())
)
# Use the metadata to create the table
metadata.create_all(engine)
# Print table details
print(repr(data))
```

#### insert data

> use an `insert` statement where you specify the table as an argument, and supply the data you wish to insert into the value via the `.values()` method as keyword arguments (`column=value`).

```
# Build an insert statement to insert a record into the data table: insert_stmt
insert_stmt = insert(data).values(name='Mary', count=1, amount=1000.00, valid=True)
# Execute the insert statement via the connection: results
results = connection.execute(insert_stmt)
# Print result rowcount
print(results.rowcount)
# Build a select statement to validate the insert: select_stmt
select_stmt = select([data]).where(data.columns.name == 'Mary')
# Print the result of executing the query.
print(connection.execute(select_stmt).first())
```

> when inserting multiple records at once, you do not use the `.values()` method. Instead, you'll want to first build a **list of dictionaries** that represents the data you want to insert, with keys being the names of the columns. in the `.execute()` method, you can pair this list of dictionaries with an insert statement, which will insert all the records in your list of dictionaries.

```
# Build a list of dictionaries: values_list
values_list = [
    {'name': 'Mary', 'count': 1, 'amount': 1000.00, 'valid': True},
    {'name': 'John', 'count': 1, 'amount': 750.00, 'valid': False}
]
# Build an insert statement for the data table: stmt
stmt = insert(data)
# Execute stmt with the values_list: results
results = connection.execute(stmt, values_list)
# Print rowcount
print(results.rowcount)
```
> to load the contents of a CSV file into a table, you can do it quicky through a pandas DataFrame: you can call the `.to_sql()` method on the DataFrame to load it into a SQL table in a database. The columns of the DataFrame should match the columns of the SQL table. The parameters are:
* `name` is the name of the SQL table (as a string).
* `con` is the connection to the database that you will use to upload the data.
* `if_exists` specifies how to behave if the table already exists in the database; possible values are `"fail"`, `"replace"`, and `"append"`.
* `index` (True or False) specifies whether to write the DataFrame's index as a column.* 

> if the table already esist and we want to append the data... specify so

#### update 

The `update` statement is very similar to an `insert` statement

```
stmt = update(employees).values(wage=100.00)
```

>  a `where` clause on the statement will help us determine what data to update


#### delete

* You can empty a table with a `delete` statement with just the table as an argument.

>  a `where` clause on the statement will help us determine what data to delete

* to drop individual tables from a database use the `.drop()` method, 

* to drop all tables in a database with the `.drop_all()` method

> you can check to see if a table exists on an engine with the `.exists(engine)` method.




[the documentation]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#module-sqlalchemy.sql.expression