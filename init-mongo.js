
db.auth("username", "password");
db = db.getSiblingDB('foo_db');
db.createUser(
    {
        user: "userman",
        pwd: "userpwd",
        roles:[
            {
            role: "readWrite",
            db: "foo_db"
            },
        ],
            
    }
);

//db = new Mongo().getDB("foo_db")

db.createCollection('tests', {capped:false});


db.tests.insert([
    {"integer": 1, "string" : "this is a string"},
    {"integer": 2, "string" : "Name"}
]);