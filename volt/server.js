var pages = process.argv[2];
var port = process.argv[3];

// Start express server
const express = require("express");
const server = express();
server.use(express.static(pages));
server.listen(port, function() {
    console.log("Starting to serve pages on port " + port);
});
