const express = require('express');
const bcrypt = require('bcrypt');
const db= require('./db');
const router = express.Router();
const jwt = require('jsonwebtoken');

const SECRET = 'v8Q!z&7P@kR#2sM$gT*F9nL0bX!uCwYd';


// tasksdb.run(
//     `CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id Integer, task TEXT,title TEXT,description TEXT,effort_to_complete INTEGER,due_date DATE)`
//         );





function authenticaTetoken(req, res, next) {
    console.log("Authorization",req,res)
    const token = req.headers['Authorization']?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ message: 'Token required' });
    }

    try {
        // Verify the token and decode the payload at the same time
        const decoded = jwt.verify(token, SECRET_KEY);
        // const decoded = jwt.decode(token, SECRET_KEY);

        // Store the decoded data in req.data
        req.data = decoded;

        // Pass control to the next middleware/route handler
        next();
    } catch (err) {
        return res.status(403).json({ message: 'Invalid or expired token' });
    }
}


// Register     
router.post('/register', (req, res) => {
    console.log('req.body', req.body)
    const {username, password} = req.body;
    console.log("email and pass", username, password)
    const hash = bcrypt.hashSync(password, 10);
    db.run(`INSERT INTO user (username, password) VALUES (?, ?)`, [username, hash], function(err) {
        if (err) {
            if (err.code === 'SQLITE_CONSTRAINT') {
                return res.status(409).json({ message: 'User already exists' });
            }
            return res.status(500).json({ message: 'Database error' });
        }else {
            return res.status(201).json({ message: 'User registered successfully' });
        }
    });
});

// Login
router.post('/login', (req, res) => {
    const {username, password} = req.body;
    db.get(`SELECT * FROM user WHERE username = ?`, [username], (err, user) => {
        if (err || !user) return res.status(404).json({ message: "User not found" });
        const isValid = bcrypt.compareSync(password, user.password);
        if (!isValid) return res.status(401).send("Wrong Password");
        const token = jwt.sign({id:user.id, username:user.username}, SECRET,  { expiresIn: '30m' });
        res.json({ token });
    });
});
     
// router.post('/task_add', authenticaTetoken, (req, res) => {
//     console.log('req.body', req.body);

//     const { title, description,task, etc, due_date } = req.body;

//     // Extract user info from req.data (which comes from the JWT)
//     const { id, username } = req.data;
//     // const id = 6
//     // Check if the task already exists for the user (unique by title or other criteria)
//     tasksdb.get(`SELECT * FROM tasks WHERE user_id = ? AND title = ?`, [id, title], (err, row) => {
//         if (err) {
//             console.error(err);
//             return res.status(500).json({ message: 'Database error' });
//         }

//         if (row) {
//             // If task exists, return a message without throwing an error
//             return res.status(200).json({ message: 'Task already exists' });
//         }

//         // If task does not exist, insert it into the database
//         tasksdb.run(`INSERT INTO tasks (user_id, title, task, description, effort_to_complete, due_date) 
//                 VALUES (?, ?, ?, ?, ?, ?)`, 
//                 [id, title, task, description, etc, due_date], 
//                 function(err) {
//             if (err) {
//                 console.error(err);
//                 return res.status(500).json({ message: 'Database error' });
//             } else {
//                 return res.status(201).json({ message: 'Task added successfully' });
//             }
//         });
//     });
// });


// router.put('/task_update', authenticaTetoken, (req, res) => {
//     const { title } = req.body;
//     const { id } = req.data; // user_id from JWT

//     if (!title) {
//         return res.status(400).json({ message: 'Title is required' });
//     }

//     // Check if task exists for this user
//     tasksdb.get(`SELECT * FROM tasks WHERE user_id = ? AND title = ?`, [id, title], (err, row) => {
//         if (err) {
//             console.error(err);
//             return res.status(500).json({ message: 'Database error' });
//         }

//         if (!row) {
//             return res.status(404).json({ message: 'Task not found for this user' });
//         }

//         // Toggle status from 'complete' to 'incomplete' or vice versa
//         const newStatus = row.status === 'complete' ? 'incomplete' : 'complete';

//         // Update the task's status
//         tasksdb.run(`UPDATE tasks SET status = ? WHERE user_id = ? AND title = ?`, 
//             [newStatus, id, title], 
//             function(err) {
//                 if (err) {
//                     console.error(err);
//                     return res.status(500).json({ message: 'Database error' });
//                 }

//                 return res.status(200).json({ 
//                     message: `Task status updated to ${newStatus}`, 
//                     updated_status: newStatus 
//                 });
//             });
//     });
// });

// router.get('/task_get', authenticaTetoken, (req, res) => {
//     const { title } = req.query;
//     const { id } = req.data; // user_id from JWT

//     if (!title) {
//         return res.status(400).json({ message: 'Title is required as query parameter' });
//     }

//     // Fetch the task based on user_id and title
//     tasksdb.get(`SELECT * FROM tasks WHERE user_id = ? AND title = ?`, [id, title], (err, row) => {
//         if (err) {
//             console.error(err);
//             return res.status(500).json({ message: 'Database error' });
//         }

//         if (!row) {
//             return res.status(404).json({ message: 'Task not found' });
//         }

//         return res.status(200).json({
//             message: 'Task fetched successfully',
//             task: row
//         });
//     });
// });

// router.delete('/task_delete', authenticaTetoken, (req, res) => {
//     const { title } = req.body;
//     const { id } = req.data; // user_id from JWT

//     if (!title) {
//         return res.status(400).json({ message: 'Title is required in body' });
//     }

//     // Check if the task exists
//     tasksdb.get(`SELECT * FROM tasks WHERE user_id = ? AND title = ?`, [id, title], (err, row) => {
//         if (err) {
//             console.error(err);
//             return res.status(500).json({ message: 'Database error' });
//         }

//         if (!row) {
//             return res.status(404).json({ message: 'Task not found' });
//         }

//         // Delete the task
//         tasksdb.run(`DELETE FROM tasks WHERE user_id = ? AND title = ?`, [id, title], function(err) {
//             if (err) {
//                 console.error(err);
//                 return res.status(500).json({ message: 'Database error during deletion' });
//             }

//             return res.status(200).json({ message: 'Task deleted successfully' });
//         });
//     });
// });


module.exports = router;


