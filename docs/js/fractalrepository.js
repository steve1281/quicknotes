var bluerose = function() {
  var red = function(i, j) {
    var a = 0,
      b = 0,
      c, d, n = 0;
    while ((c = a * a) + (d = b * b) < 4 && n++ < 880) {
      b = 2 * a * b + j * 8e-9 - 0.645411;
      a = c - d + i * 8e-9 + 0.356888;
    }
    return 255 * Math.pow((n - 80) / 800, 3.0);
  };

  var green = function(i, j) {
    var a = 0,
      b = 0,
      c, d, n = 0;
    while ((c = a * a) + (d = b * b) < 4 && n++ < 880) {
      b = 2 * a * b + j * 8e-9 - 0.645411;
      a = c - d + i * 8e-9 + 0.356888;
    }
    return 255 * Math.pow((n - 80) / 800, 0.7);
  };

  var blue = function(i, j) {
    var a = 0,
      b = 0,
      c, d, n = 0;
    while ((c = a * a) + (d = b * b) < 4 && n++ < 880) {
      b = 2 * a * b + j * 8e-9 - 0.645411;
      a = c - d + i * 8e-9 + 0.356888;
    }
    return 255 * Math.pow((n - 80) / 800, 0.5);
  };

  return {
    "red": red,
    "green": green,
    "blue": blue
  };
};

var flag = function() {

  var red = function red(x, y) {
    if (x > 600 || y > 560) return 1024;
    x += 35, y += 41;
    return y % 124 < 20 && x % 108 < 20 ? 1024 : (y + 62) % 124 < 20 && (x + 54) % 108 < 20 ? 1024 : 0;
  };

  var green = function green(x, y) {
    if (x > 600 || y > 560) return y % 160 < 80 ? 0 : 1024;
    x += 35, y += 41;
    return y % 124 < 20 && x % 108 < 20 ? 1024 : (y + 62) % 124 < 20 && (x + 54) % 108 < 20 ? 1024 : 0;
  };

  var blue = function blue(x, y) {
    return ((x > 600 || y > 560) && y % 160 < 80) ? 0 : 1024;
  };

  return {
    "red": red,
    "blue": blue,
    "green": green
  };
};

var mandel = function() {
  var red = function(i, j) {
    var x = 0;
    var y = 0;
    var k;
    for (k = 0; k++ < 256;) {
      var a = x * x - y * y + (i - 768.0) / 512;
      y = 2 * x * y + (j - 512.0) / 512;
      x = a;
      if (x * x + y * y > 4) break;

    }
    return k > 31 ? 256 : k * 8;
  };

  var green = function(i, j) {
    var x = 0;
    var y = 0;
    var k;
    for (k = 0; k++ < 256;) {
      var a = x * x - y * y + (i - 768.0) / 512;
      y = 2 * x * y + (j - 512.0) / 512;
      x = a;

      if (x * x + y * y > 4) break;

    }
    return k > 63 ? 256 : k * 4;

  };

  var blue = function(i, j) {
    var x = 0;
    var y = 0;
    var k;
    for (k = 0; k++ < 256;) {
      var a = x * x - y * y + (i - 768.0) / 512;
      y = 2 * x * y + (j - 512.0) / 512;
      x = a;
      if (x * x + y * y > 4)
        break;

    }
    return k;

  };

  return {
    "red": red,
    "blue": blue,
    "green": green
  };
};


var topdownpyr = function() {

  var red = function(i, j) {
    return i && j ? (i % j) & (j % i) : 0;
  };

  var green = function(i, j) {
    return i && j ? (i % j) + (j % i) : 0;
  };

  var blue = function(i, j) {
    return i && j ? (i % j) | (j % i) : 0;

  };

  return {
    "red": red,
    "blue": blue,
    "green": green
  };
};


var devon = function() {
 
var red= function(x,y){
  return (x % y);
  //return 1024 * (Math.tan(x - y) + Math.tan(x + y));
}

var green = function(x,y){
  return (y % x);
  //return 1024 * (Math.sin(x - y) + Math.sin(x + y));
}

var blue = function(x,y) {
  return Math.sin(x % y + y % x) * 500;
  //return 1024 * (Math.cos(x - y) + Math.cos(x + y));
}
  return {
    "red": red,
    "blue": blue,
    "green": green
  };
}


var none = function() {
  var red = function(i, j) {
    return 100;
  };

  var green = function(i, j) {
    return 100;
  };

  var blue = function(i, j) {
    return 100;

  };

  return {
    "red": red,
    "blue": blue,
    "green": green
  };
}
