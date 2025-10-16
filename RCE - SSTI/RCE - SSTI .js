const express = require('express')
const ejs = require('ejs')
const { log } = require('console')

const app = express()
const port = 3000

app.set("view engine", "ejs")

app.get("/", (req, res) => {
    var template = `<h1>${req.query.payload}</h1>`
    return res.send(ejs.render(template))
})

app.listen(port, () => log(`Listen On http://localhots:${port}`))