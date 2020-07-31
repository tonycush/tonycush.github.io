var loco_path = window.location.pathname;
res = loco_path.substring(15);
if(res.length >1){
  ht_ind = res.indexOf(".html");
  actual_loco = res.substring(1,ht_ind);
} else{
  actual_loco = "Home"
}

document.write('\
<nav class="navbar navbar-expand-sm bg-primary navbar-dark fixed-top">\
  <ul class="navbar-nav">\
    <li class="nav-item">\
      <a class="nav-link" href="index.html">Home</a>\
    </li>\
    <li class="nav-item">\
      <a class="nav-link " href="#">Graph</a>\
    </li>\
    <li class="nav-item">\
      <a class="nav-link" href="#">Fancy Feature</a>\
    </li>\
  </ul>\
</nav>\
');

document.write();

document.write('\
<div class="jumbotron text-center">\
  <h1>WHO WRITE\'S THIS</h1>\
  <p>Who is or ever was!</p>\
</div>\
');