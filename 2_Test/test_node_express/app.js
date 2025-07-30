const express = require('express');
const app = express();
const session = require('express-session');
const configRoutes = require('./routes');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/public/'));

app.use(
    session({
        name: 'AuthCookie',
        secret: "This is a secret.. shhh don't tell anyone",
        saveUninitialized: true,
        resave: false
    })
);

app.use("*", (req, res, next) => {
    let log = `[${new Date().toUTCString()}]:${req.method} ${req.originalUrl}`;
    if (req.session.user) {
        log += ' (Authenticated User)';
    } else {
        log += ' (Non-Authenticated User)';
    }
    console.log(log);
    next();
});

app.use("*", (req, res, next) => {
    if (!req.session.user) {
        if (req.method == "PUT" || req.method == "POST" || req.method == "PATCH") {
            if ((req.originalUrl != "/blog/login" && req.originalUrl != "/blog/signup")) {
                res.status(403).json({ "error": "user not loged in" });
                return;
            }
        }
    }
    next();
});

app.use("*", (req, res, next) => {
    if (req.method == "POST" && /^\/blog\/[0-9a-zA-Z]+\/comments$/.test(req.originalUrl) && !req.session.user) {
        res.status(403).json({ "error": "user not loged in" });
        return;
    }
    if (req.method == "DELETE" && /^\/blog\/[0-9a-zA-Z]+\/[0-9a-zA-Z]+$/.test(req.originalUrl) && !req.session.user) {
        res.status(403).json({ "error": "user not loged in" });
        return;
    }
    next();
});

configRoutes(app);

app.listen(3000, () => {
    console.log("We've now got a server!");
    console.log('Your routes will be running on http://localhost:3000');
});
