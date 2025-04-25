const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const routes = require('./routes');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/api/auth', routes);

app.listen(3001,() => {console.log('Auth-Server is running on port 3001')});
