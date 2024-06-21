var title = document.querySelector('.top h1');
var banner = document.querySelector('.top img');
var webname = document.querySelector('.top h2');
const banners = ["assets/480 120 banner 2x.gif", "assets/A-star banner.gif"]
function titleChange(){
    var width = innerWidth;
    console.log(width);
    if (width > 1280){
        title.style.fontSize = 0.0055*width + 'em';
        webname.style.fontSize = 0.003*width + 'em';
        console.log(title.style.fontSize);
    }
    else{
        title.style.fontSize = 0.0055*1280 + 'em';
        webname.style.fontSize = 0.003*1280 + 'em';
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