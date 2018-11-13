// test.js
var page = require('webpage').create(), //获取操作dom或web网页的对象
    system = require('system'),         //获取操作系统对象
    address;
if (system.args.length === 1) {
    phantom.exit(1);
} else {
    address = system.args[1];
    page.open(address, function (status) {   //访问url
        console.log(page.content);
        phantom.exit();
    });
}