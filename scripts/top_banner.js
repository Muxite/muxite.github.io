var title = document.querySelector('.top h1');
var banner = document.querySelector('.banner');
var webname = document.querySelector('.top h2');
var title_name = document.title;
var title_ratio = 0.06;
var webname_ratio = 0.03;
const banners = ["assets/480 120 banner 2x.gif", "assets/A-star banner.gif"]
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
    var pick = banners[Math.floor(Math.random() * banners.length)];
    banner.src = pick;
    title.innerHTML = title_name;
    titleChange();
};