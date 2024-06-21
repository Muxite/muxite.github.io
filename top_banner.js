var title = document.querySelector('.top h1');
var webname = document.querySelector('.top h2');

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
    titleChange();
};