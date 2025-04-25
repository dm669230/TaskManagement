const express = require('express');
const bcrypt = require('bcrypt');
const db= require('./db');
const router = express.Router();
const jwt = require('jsonwebtoken');

const SECRET = 'v8Q!z&7P@kR#2sM$gT*F9nL0bX!uCwYd';

function authenticaTetoken(req, res, next) {
    console.log("Authorization",req,res)
    const token = req.headers['Authorization']?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ message: 'Token required' });
    }

    try {
        const decoded = jwt.verify(token, SECRET_KEY);
        req.data = decoded;
        console.log("Decoded", decoded)
        next();
    } catch (err) {
        return res.status(403).json({ message: 'Invalid or expired token' });
    }
}


// Register  api   
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

// Login api
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
 

module.exports = router;


