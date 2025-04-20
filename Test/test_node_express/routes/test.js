const express = require('express');
const router = express.Router();
const { check } = require("../public/js/check");
const { blog } = require("../data");
const { comment } = require("../data");
const { user } = require("../data");

router.get('/', async (req, res) => {
    let errors = [];
    if (!(take = check(req.query.take, "take"))) errors.push("take");
    let skip = check(req.query.skip, "skip");
    if (skip < 0) errors.push("skip");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await blog.getAll(take, skip);
        res.status(200).json({ "blogs": data.blogs });
    } catch (error) {
        res.status(500).json(error);
    }
});

router.get('/logout', async (req, res) => {

    if (!req.session.user) {
        res.status(400).json({ "hasErrors": true, "errors": "Please log in first" });
        return;
    }

    req.session.user = null;

    res.status(200).json({ "message": "log out succussfully!" })
});

router.get('/:blog_id', async (req, res) => {
    let errors = [];
    if (!(blog_id = check(req.params.blog_id, "id"))) errors.push("blog_id");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await blog.getOne(blog_id);
        if (data.hasErrors) {
            if (data.errors.includes("blog not exist")) {
                res.status(404).json({ "error": "blog not exist" });
            }
        } else {
            res.status(200).json({ "blog": data.blog });
        }
    } catch (error) {
        res.status(500).json(error);
    }
});

router.post('/', async (req, res) => {
    let errors = [];
    if (Object.keys(req.body).length != 2) errors.push("arguments");
    if (!(title = check(req.body.title, "title"))) errors.push("title");
    if (!(body = check(req.body.body, "body"))) errors.push("body");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await blog.create(req.session.user.user_id, title, body);
        if (data.hasErrors) {
            res.status(404).json({ "error": data.errors });
        } else {
            res.status(200).json({ "blog": data.blog });
        }
    } catch (error) {
        res.status(500).json(error);
    }
});

router.put('/:blog_id', async (req, res) => {
    let errors = [];
    if (Object.keys(req.body).length != 2) errors.push("arguments");
    if (!(title = check(req.body.title, "title"))) errors.push("title");
    if (!(body = check(req.body.body, "body"))) errors.push("body");
    if (!(blog_id = check(req.params.blog_id, "id"))) errors.push("blog_id");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await blog.update(blog_id, req.session.user.user_id, title, body);
        if (data.hasErrors) {
            res.status(404).json({ "error": data.errors });
        } else {
            res.status(200).json({ "blog": data.blog });
        }
    } catch (error) {
        res.status(500).json(error);
    }
});

router.patch('/:blog_id', async (req, res) => {
    let errors = [];
    if (!(blog_id = check(req.params.blog_id, "id"))) errors.push("blog_id");
    let argu = ["title", "body"];
    for (let i = 0; i < Object.keys(req.body).length; i++) {
        if (!argu.includes(Object.keys(req.body)[i])) {
            errors.push("arguments");
        }
    }

    const specBlog = await blog.getOne(blog_id);
    let title = req.body.title, body = req.body.body;
    if (title != undefined) {
        if (!check(title, "title")) {
            errors.push("title");
        }
    } else {
        title = specBlog.blog.title;
    }
    if (body != undefined) {
        if (!check(body, "body")) {
            console.log("aa")
            errors.push("body");
        }
    } else {
        body = specBlog.blog.body;
    }
    if (title == specBlog.title && body == specBlog.body) {
        errors.push("blog not changed");
    }

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await blog.update(blog_id, req.session.user.user_id, title, body);
        if (data.hasErrors) {
            res.status(404).json({ "error": data.errors });
        } else {
            res.status(200).json({ "blog": data.blog });
        }
        res.status(200).json();
    } catch (error) {
        res.status(500).json(error);
    }
});

router.post('/:blog_id/comments', async (req, res) => {
    let errors = [];
    if (Object.keys(req.body).length != 1) errors.push("arguments");
    if (!(comm = check(req.body.comment, "comment"))) errors.push("comment");
    if (!(blog_id = check(req.params.blog_id, "id"))) errors.push("blog_id");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await comment.create(blog_id, req.session.user.user_id, comm);
        if (data.hasErrors) {
            res.status(404).json({ "error": data.errors });
        } else {
            res.status(200).json({ "blog": data.blog });
        }
    } catch (error) {
        res.status(500).json(error);
    }
});

router.delete('/:blog_id/:comment_id', async (req, res) => {
    let errors = [];
    if (!(comment_id = check(req.params.comment_id, "id"))) errors.push("comment_id");
    if (!(blog_id = check(req.params.blog_id, "id"))) errors.push("blog_id");

    
    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await comment.dele(blog_id,req.session.user.user_id,comment_id);
        if (data.hasErrors) {
            res.status(404).json({ "error": data.errors });
        } else {
            res.status(200).json({ "message": "comment delete succusfully" });
        }
    } catch (error) {
        res.status(500).json(error);
    }
});

router.post('/signup', async (req, res) => {
    if (req.session.user) {
        res.status(400).json({ "hasErrors": true, "errors": "User had loged in!" });
        return;
    }

    let errors = [];
    if (Object.keys(req.body).length != 3) errors.push("arguments");
    if (!(name2 = check(req.body.name, "name"))) errors.push("name");
    if (!(username = check(req.body.username, "username"))) errors.push("username");
    if (!(password = check(req.body.password, "password"))) errors.push("password");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await user.signup(name2, username, password);
        if (data.hasErrors) {
            res.status(400).json(data);
            return;
        }
        req.session.user = { user_id: data.user._id, username: data.user.username };
        res.status(200).json({ "user": data.user });
    } catch (error) {
        res.status(500).json(error);
    }
});

router.post('/login', async (req, res) => {
    if (req.session.user) {
        res.status(400).json({ "hasErrors": true, "errors": "User had loged in!" });
        return;
    }

    let errors = [];
    if (Object.keys(req.body).length != 2) errors.push("arguments");
    if (!(username = check(req.body.username, "username"))) errors.push("username");
    if (!(password = check(req.body.password, "password"))) errors.push("password");

    if (errors.length > 0) {
        res.status(400).json({ "hasErrors": true, "errors": errors });
        return;
    }

    try {
        const data = await user.login(username, password);
        if (data.hasErrors) {
            res.status(400).json(data);
            return;
        }
        req.session.user = { user_id: data.user._id, username: data.user.username };
        res.status(200).json({ "user": data.user });
    } catch (error) {
        res.status(500).json(error);
    }
});

module.exports = router;