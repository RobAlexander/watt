#!/bin/node

const fs = require('fs'), http = require("http"), xmldoc = require("xmldoc");

// Handle command line arguments
var url = process.argv[2], output = process.argv[3];

var acheckerId = fs.readFileSync(process.env["WATT_ROOT"] + "/acheckerid", {encoding:"utf-8"}).split("\n")[0];

http.get("http://192.168.50.101:9080/AChecker/checkacc.php?uri=" + encodeURIComponent(url) +  "&id=" + acheckerId + "&output=rest", (resp) => {
    var data = '';
    resp.on('data', (chunk) => {
        data += chunk;
    });

    resp.on("end", () => {
        var xml = new xmldoc.XmlDocument(data);
        var json = {"violations": [], "passes": [], "incomplete": [], "inapplicable": []};
        xml.childNamed("results").eachChild(function (result, index, array) {
            var errorMsgFull = result.valueWithPath("errorMsg");
            var error = new xmldoc.XmlDocument(errorMsgFull);
            var resultObject = {
                "message": errorMsgFull.substring(errorMsgFull.indexOf(">") + 1, errorMsgFull.lastIndexOf("<")),
                "id": result.valueWithPath("sequenceID"),
                "nodes": [{
                    "html": result.valueWithPath("errorSourceCode"),
                    "target": "~" + result.valueWithPath("lineNum") + ":" + result.valueWithPath("columnNum")
                }],
                "help": error.attr.href,
                "helpUrl": error.attr.href,
                "impact": result.valueWithPath("resultType")
            };
            switch (result.valueWithPath("resultType")) {
                case "Error":
                    json["violations"].push(resultObject);
                    break;
                default:
                    json["incomplete"].push(resultObject);
            }
        });

        fs.writeFileSync(output, JSON.stringify(json), 'utf8');
        process.exit(0);
    });
});
