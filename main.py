from database.mysql import MySQLDatabase
from settings import db_config
import random

"""
Retrieve the settings from the
`db_config` dictionary to connect to
our database so we can instantiate our
MySQLDatabase object
"""
db = MySQLDatabase(db_config.get('db_name'),
                   db_config.get('user'),
                   db_config.get('pass'),
                   db_config.get('host'))

# Get all the records from
# the people table
results = db.select('people')

for row in results:
    print row

# Selecting columns with named tuples
results = db.select('people',
                    columns=['id', 'first_name'], named_tuples=True)

for row in results:
    print row.id, row.first_name

# We can also do more complex queries using `CONCAT`
# and `SUM`
people = db.select('people', columns=["CONCAT(first_name, ' ', second_name)" \
                                      " AS full_name", "SUM(amount)" \
                                                       " AS total_spend"],
                   named_tuples=True, where="people.id=1",
                   join="orders ON people.id=orders.person_id")

for person in people:
    print person.full_name, "spent ", person.total_spend

# Inserting an order
db.insert('orders', person_id="2", amount="120.00")

# Updating a person
person = db.select('people', named_tuples=True)[0]

db.update('profiles', where="person_id=%s" % person.id,
          address="1a another street")

# Deleting a record
person = db.select('people', named_tuples=True)[0]
db.delete('orders', person_id="=%s" % person.id, id="=1")

# Challenge A:
# Using the AVG(), select a person from your people table
#  and get the average amount they spend and,
#  at the same time, create a column that reads,
#  first_name spends. Then print out the columns
# to provide the answers in the terminal
peopleavg = db.select('people', columns=["CONCAT(first_name, ' ', second_name)" \
                                         " AS full_name", "AVG(amount)" \
                                                          " AS avg_spend"],
                      named_tuples=True, where="people.id=2",
                      join="orders ON people.id=orders.person_id")

for person in peopleavg:
    print person.full_name, "spent on average ", person.avg_spend

# Challenge B:
# Create a new person in the people table and
# add in a profile row and two orders of random value.

db.insert('people', first_name="Caroline", second_name="Greene", DOB='STR_TO_DATE("27-11-1971", "%d-%m-%Y")')
caroline = db.select('people', ["id", 'first_name'], where='first_name="Caroline"', named_tuples=True)[0]
db.insert('profiles', person_id="%s" % caroline.id, address="Turnings, Straffan")
db.insert('orders', person_id="%s" % caroline.id, amount='%s' % random.randint(1,30))
db.insert('orders', person_id="%s" % caroline.id, amount='%s' % random.randint(5,67))
orders = db.select('orders', where='person_id=%s' % caroline.id)

for order in orders:
    print order

# Challenge C:
# Once youve added them in use select to get
# their full name and the minimum amount they have spent.

personCaroline = db.select('people', columns=["CONCAT(first_name, ' ', second_name)"
                                      " AS full_name", "MIN(amount)"
                                      " AS min_spend"],
                   named_tuples=True, where="people.first_name='Caroline'",
                   join="orders ON people.id=orders.person_id")

print personCaroline

# Challenge D:
# Choose a person and update ALL of his orders to have the amount 20.02.

tess = db.select('people', ["id", 'first_name'], where='first_name="Tess"', named_tuples=True)[0]
print tess

tess_orders = db.select('orders', named_tuples=True, where='person_id=%s' % tess.id)
print tess_orders

for order in tess_orders:
    print order
    db.update('orders', where="id=%s" % order.id, amount="20.02")

new_tess_orders = db.select('orders', named_tuples=True, where='person_id=%s' % tess.id)

for order in new_tess_orders:
    print order

# challenge E would cause all orders to be deleted






