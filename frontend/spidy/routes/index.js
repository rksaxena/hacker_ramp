var express = require('express');
var router = express.Router();
var request = require('request');

/* GET home page. */
router.get('/',
  function(req, res, next) {
  res.render('index', { title: 'Home' });
});
router.get('/selectionGap',
    function(req,res){
    res.render('selection_gap')
});
router.get('/trending',
    function(req,res){
    res.render('trending')
});
router.get('/getSelectionGap',function(req,res)
{
    request("http://192.168.12.155:12313/tags/all", function(error, response, body) {
    //console.log(body);
    res.send(body);
    });
});
router.get('/getTrending',function(req,res){
    request('http://192.168.12.155:12313/tags/ranks',function(error,response,body){
        console.log(body);
        res.send(body);
    })
})

module.exports = router;
