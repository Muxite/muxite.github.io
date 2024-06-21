var title = document.querySelector('.top h1');
var banner = document.querySelector('.top img');
var webname = document.querySelector('.banner');
const banners = ["assets/480 120 banner 2x.gif", "assets/A-star banner.gif"]
function titleChange(){
    var width = innerWidth;
    console.log(width);
    if (width > 1280){
        title.style.fontSize = 0.005*width + 'em';
        webname.style.fontSize = 0.0025*width + 'em';
        console.log(title.style.fontSize);
    }
    else{
        title.style.fontSize = 0.005*1280 + 'em';
        webname.style.fontSize = 0.0025*1280 + 'em';
        console.log(title.style.fontSize);
    }
}

// Event listener for window resize
window.addEventListener('resize', titleChange);

window.onload = function() {
    var pick = banners[Math.floor(Math.random() * banners.length)];
    banner.src = pick;
    titleChange();
};