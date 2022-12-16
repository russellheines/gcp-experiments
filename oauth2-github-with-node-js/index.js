const express = require('express');
const app = express();

const axios = require('axios');

function getuser(token) {
  axios.get('https://api.github.com/user', 
  {
	  headers: { Authorization: 'Bearer ' + token }
  })
  .then(function (response) {
	console.log(response.data.name);
  })
  .catch(function (error) {
    console.log(error);
  });  
}

function gettoken(code) {
  axios.post('https://github.com/login/oauth/access_token', {
    client_id: '7dbd0a9f61d655243969',
    client_secret: 'CHANGEME',
    code: code
  },
  {
	  headers: { Accept: 'application/json' }
  })
  .then(function (response) {
	console.log(response.data.access_token);
	getuser(response.data.access_token);
  })
  .catch(function (error) {
    console.log(error);
  });
}

app.get('/', function (req, res) {
  res.send('<a href="https://github.com/login/oauth/authorize?client_id=7dbd0a9f61d655243969">Login with Github</a>');
});

app.get('/login/oauth2/code/github', function (req, res) {
	console.log(req.query.code);
	gettoken(req.query.code);
	
	res.send("Welcome!");
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});