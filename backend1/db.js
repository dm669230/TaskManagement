const sqlite3 = require('sqlite3').verbose();
// const db = new sqlite3.Database('user.db');
const db = new sqlite3.Database('../database/main.db', (err) => {
    if (err) {
        console.error('Error opening database', err);
    } else {
        console.log('Connected to the shared SQLite database');
    }
});
// const tasksdb = new sqlite3.Database('tasks.db');

db.run(
    `CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)`
        );
db.run(
    `CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT,
    status TEXT, description TEXT, etc INTEGER, due_date TEXT);`
        );


module.exports = db;