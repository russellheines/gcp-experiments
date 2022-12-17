const express = require('express');
const app = express();

const axios = require('axios');

function getuser(token) {
  axios.get('https://www.googleapis.com/oauth2/v2/userinfo', 
  {
	  headers: { Authorization: 'Bearer ' + token }
  })
  .then(function (response) {
	console.log(response.data);
  })
  .catch(function (error) {
    console.log(error);
  });  
}

function gettoken(code) {
  axios.post('https://oauth2.googleapis.com/token', {
    client_id: '708733497091-l3njp9vfnni4v5misr1b2fepgbr4409t.apps.googleusercontent.com',
    client_secret: 'CHANGEME',
    redirect_uri: 'http://localhost:3000/login/oauth2/code/google',
    grant_type: 'authorization_code',
    code,
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
	
	const p1 = "scope=https%3A//www.googleapis.com/auth/userinfo.email";
  	const p2 = "redirect_uri=http%3A//localhost%3A3000/login/oauth2/code/google";
	const p3 = "access_type=offline";
	const p4 = "response_type=code";
	const p5 = "client_id=708733497091-l3njp9vfnni4v5misr1b2fepgbr4409t.apps.googleusercontent.com";
	const url = "https://accounts.google.com/o/oauth2/v2/auth?" + p1 + "&" + p2 + "&" + p3 + "&" + p4 + "&" + p5; 
	
 	res.send('<a href="' + url + '">Login with Google</a>');
});

app.get('/login/oauth2/code/google', function (req, res) {
	console.log(req.query.code);
	gettoken(req.query.code);
	
	res.send("Welcome!");
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});