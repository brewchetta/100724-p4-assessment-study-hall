# Phase 4 Study Guide


1. What is a server? What are routes? What are RESTful routes? What are dynamic routes? What is CRUD?

```
SERVER: A place to store data. People can access the data on the server. There are multiple types of servers, for example servers that serve HTML, or info from a database, or anything else.

ROUTE: This is usually a location within a server, a place we can get to for specific things.

DYNAMIC ROUTE: If you wanted to get a cat by an :id that would be a dynamic route since we aren't hard-coding each cat's :id. Generally tied to route parameters.

RESTful ROUTES: This makes your routes predictable - makes it easier for others to access your resources
index       - GET       /cats
show        - GET       /cats/:id
create      - POST      /cats
update      - PATCH     /cats/:id
destroy     - DELETE    /cats/:id

CRUD: Create, Read, Update, Delete
```

2. What is a model? How does it relate to python and databases? What does the command `flask db migrate -m "new message"` do? What is a migration? What does the command `flask db upgrade` do?

```
MODEL: Relates to a table in our database. The model is the python class that interacts with a specific table. For example the Cat model will do things with the `cats_table`. Models usually work with just one table.

MIGRATION: It's like staging, getting a new version ready to be set up for our database based on the models we've built. This doesn't affect the database yet.

UPGRADE: Uses the latest version(s) to create the tables. The tables will have column names but won't add in any additional rows.

SEED: If we want to seed we would then have to run a seed file.
```


3. How can we introduce a relationship between two models? (HINT: What columns and special code do those models need?)  What is the difference between a one to many and a many to many?

```python

# one to many --> one professor has many students

class Professor(db.Model):
    # stuff goes here

    __tablename__ == 'professors_table'

    id = db.Column(db.Integer, primary_key=true) # the id is unique --> primary key

    students = db.relationship('Student', back_populates='professor')
                                # classname     # the name of the relationship in Student


class Student(db.Model):
    # stuff goes here

    id = db.Column(db.Integer, primary_key=true) # the id is unique --> primary key

    professor_id = db.Column(db.Integer, db.ForeignKey('professors_table.id')) # fk goes in the many side

    professor = db.relationship('Professor', back_populates='students')
                                # classname     # the name of the relationship in Professor
```


```python
from sqlalchemy.ext.associationproxy import association_proxy # need this for our many to many

class Driver(db.Model):
    
    __tablename__ = 'drivers_table'

    id = db.Column(db.Integer, primary_key=true)

    cars = db.relationship('Car', back_populates='driver')

    manufacturers = association_proxy('cars', 'manufacturer')
    # go through cars relationship and grab each manufacturer


class Car(db.Model): # this is the join table

    __tablename__ = 'cars_table'

    id = db.Column(db.Integer, primary_key=true)

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers_table.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers_table.id'))

    driver = db.relationship('Driver', back_populates='cars')
    manufacturer = db.relationship('Manufacturer', back_populates='cars')

class Manufacturer(db.Model):

    __tablename__ = 'manufacturers_table'

    id = db.Column(db.Integer, primary_key=true)

    cars = db.relationship('Car', back_populates='manufacturer')

    drivers = association_proxy('cars', 'driver')
```



4. What does it mean to serialize our data and why do we do it? What does `to_dict` do? What package creates our `to_dict` for us?

```python
from sqlalchemy_serializer import SerializerMixin

class Cat(db.Model, SerializerMixin):

    __tablename__ = 'cats_table'

    id = db.Column(db.Integer, primary_key=true)
    name = db.Column(db.String)
    hungry = db.Column(db.Integer)

    toys = db.relationship(blah blah blah)

    # def to_dict(self): <<<< this gets written for us by Serializer Mixin >>>>
    #     return {
    #         id: self.id,
    #         name: self.name,
    #         hungry: self.hungry
    #     }

    def say_how_hungry(self):
        return f"{self.name} is {self.hungry} on the hungry-meter"


    serialize_rules = ('-hungry', 'say_how_hungry', '-toys.cat') # this will remove the hungry attribute from the dictionary
    # this will also include say_how_hungry in the dictionary

class Toy(db.Model, SerializerMixin):
    # belongs to cat

    cat = db.relationship(blah blah blah)

    serialize_rules = ('-cat.toys',)
    # this prevents infinite loops, we see the associated cat but not its toys

@app.get('/cats')
def get_all_cats():
    all_cats = Cat.query.all()
    return [cat.to_dict() for cat in all_cats], 200
    # to_dict transforms it into a dictionary to be sent as json

@app.get('/cat-names')
def get_all_cats():
    all_cats = Cat.query.all()
    return [cat.to_dict(rules=['-id', '-hungry']) for cat in all_cats], 200
    # can add rules for specific routes inside the .to_dict
```

5. What are validations? How do we add a validation to a model?

```python
from sqlalchemy.orm import validates
# validates is a DECORATOR

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=true)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    some_other_year = db.Column(db.Integer)
    author_name = db.Column(db.String)

    # limit the year so that it's between a reasonable earlier year and today
    @validates('publication_year')
    def validate_year(self, key, value):
        # value is what someone put in to validate
        # test for negatives
        if not isinstance(value, int):
            raise ValueError("Year must be an integer")

        if not (1920 < value < 2025):
            raise ValueError("Year must be between 1920 and 2025")

        # if it passes we return the value
        return value
```

6. There will be a debugging section. To prepare for this, assume you will either have to debug a model or a route that has invalid code.