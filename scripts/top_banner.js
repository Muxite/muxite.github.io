var title = document.querySelector('.top h1');
var webname = document.querySelector('.top h2');
var title_name = document.title;
var title_ratio = 0.04;
var webname_ratio = 0.022;
function titleChange(){
    var width = innerWidth;
    if (width > 1280){
        title.style.fontSize = title_ratio*width/title_name.length + 'em';
        webname.style.fontSize = webname_ratio*width/webname.innerHTML.length + 'em';
    }
    else{
        title.style.fontSize = title_ratio/title_name.length*1280 + 'em';
        webname.style.fontSize = webname_ratio/webname.innerHTML.length*1280 + 'em';
    }
}

// Event listener for window resize
window.addEventListener('resize', titleChange);

window.onload = function() {
    title.innerHTML = title_name;
    titleChange();
};