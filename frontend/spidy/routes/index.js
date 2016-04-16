var express = require('express');
var router = express.Router();
var request = require('request');

/* GET home page. */
router.get('/',
  function(req, res, next) {
  res.render('index', { title: 'Home' });
});
router.get('/getSelectionGap',function(req,res)
{
    request("http://localhost:9905/getSelectionGap", function(error, response, body) {
    //console.log(body);
    res.send(body);
});
})
module.exports = router;
