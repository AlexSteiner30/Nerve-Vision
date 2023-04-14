const express = require('express');

const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const cookieParser = require('cookie-parser');
const session = require('express-session');

require('dotenv').config()

const app = express();

app.use(bodyParser.urlencoded({extended: true})); 

app.use(cookieParser());
app.use(session({secret: process.env.SECRET}));

app.set('view engine', 'ejs'); 
app.use(express.static(__dirname + '/static'));

const userSchema ={
    mail: String,
    psw: String
}
  
const users = mongoose.model('users', userSchema)

app.get('/',async function(req, res){
    if(req.session.mail != null){  
        users.find({ mail: req.session.mail, psw:req.session.psw}).then( function(x){
            res.render('index-logged');
        });
    }

    else{
        res.render('index');
    }
});

app.get('/login', function(req, res){
    res.render('login');
});

app.post('/login', async function(req, res){
    const mail = req.body.mail;
    const psw = req.body.psw;

    users.find({ mail: mail, psw:psw}).then(function(x){
        if(x.length != 0){
            req.session.mail = mail;
            req.session.psw = psw;

            res.render('index-logged');
        }
        else{
            res.send('Wrong data');
        }
    });

});

app.get('/signup', function(req, res){
    res.render('signup');
});

app.post('/signup', function(req, res){
    const name = req.body.mail;
    const psw = req.body.psw;

    const newUser = new users({
        mail: name,
        psw: psw
    })

    users.create(newUser);

    res.render('login');
});


app.get('/logout', function(req, res){
    req.session.mail = null;
    req.session.password = null;

    res.render('index');
});

app.get('/generation', function(req, res){
    if(req.session.mail != null){
        res.render('generation');
    }
    else{
        res.render('index')
    }
});

app.get('/download', function(req, res){
    var path = 'static/generation.glb';
});

app.listen(port=8080, function(){
    console.log('Server is running on port 8080');

    mongoose.connect(process.env.MONGO_URI);
    console.log('Connect to the DB!');
});