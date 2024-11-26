document.addEventListener("DOMContentLoaded", function () {
    var slider = document.getElementById("voltage-slider");
    var output = document.getElementById("colored-box");
    var sliderText = document.getElementById("slider-text");
    var redText = document.getElementById("red-text");
    var greenText = document.getElementById("green-text");
    function sigmoid(x) {
        return 1 / (1 + Math.exp(-x));
    }
    
    function voltageToColorOld(voltage) {
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

    function sigmoidInterpolate(val, x1, y1, x2, y2) {
        var xc = (x1 + x2) / 2; // center point
        var k = 10 / (x2 - x1); // steepness
        return y1 + (y2 - y1) / (1 + Math.exp(-k * (val - xc)));
    }
    
    function voltageToColor(voltage) {
        var high = 24.4;
        var low = 22.2;
        var yellow = (high + low)/2
        var red = 0;
        var green = 200;

        if (voltage <= low)
        {
            red = 200;
            green = 0;
        }
        else if (low < voltage && voltage <= yellow)
        {
            red = 200;
            green = sigmoidInterpolate(voltage, low, 0, yellow, 200);
        }
        else if (yellow < voltage && voltage < high)
        {
            red = sigmoidInterpolate(voltage, yellow, 200, high, 0);
            green = 200;
        }
        else
        {
            green = 200;
            red = 0;
        }


        var r = red;
        var g = green;

        var b = 0;
        sliderText.textContent = `voltage: ${voltage}V`;
        output.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        redText.textContent = Math.round(r*10)/10;
        greenText.textContent = Math.round(g*10)/10;
    }


    function updateColor() {
        var voltage = slider.value/100;
        voltageToColor(voltage);
    }

    updateColor();
    slider.oninput = updateColor;
});