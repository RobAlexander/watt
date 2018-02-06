#!/usr/bin/phantomjs

var page = require('webpage').create();
var args = require('system').args;

if (args.length > 2) {
    page.customHeaders={'Authorization': 'Basic '+btoa(args[2] + ':' + args[3])};
}

page.settings.loadImages = true;

page.open(args[1], function() {
    page.plainText;
    var render = page.renderBase64('PNG');
    console.log(render);
    phantom.exit();
});
