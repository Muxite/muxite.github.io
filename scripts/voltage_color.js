document.addEventListener("DOMContentLoaded", function () {
    var slider = document.getElementById("voltage-slider");
    var output = document.getElementById("colored-box");
    var sliderText = document.getElementById("slider-text");
    var redText = document.getElementById("red-text");
    var greenText = document.getElementById("green-text");
    function sigmoid(x) {
        return 1 / (1 + Math.exp(-x));
    }

    function voltageToColor(voltage) {
        var high = 24.4;
        var low = 22.2;
        
        var adjustedValue = (voltage - low)/(high-low)
        var midpoint = 0.5;
        var normalizedValue = (adjustedValue - midpoint)*3;

        // Apply sigmoid function
        var sigmoidValue = sigmoid(normalizedValue);

        // Calculate RGB values
        var red = 255 * ((1 - sigmoidValue));
        var green = 255 * (sigmoidValue);
        if (red > green)
        {
            var g = green * 255/red;
            var r = 255;
        }
        else{
            var r = red * 255/green;
            var g = 255;
        }
        var b = 0;
        sliderText.textContent = `voltage: ${voltage}V`;
        output.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        redText.textContent = Math.round(r*10)/10;
        greenText.textContent = Math.round(g*10)/10;
    }

    function updateColor() {
        var voltage = slider.value/10;
        voltageToColor(voltage);
    }

    updateColor();
    slider.oninput = updateColor;
});