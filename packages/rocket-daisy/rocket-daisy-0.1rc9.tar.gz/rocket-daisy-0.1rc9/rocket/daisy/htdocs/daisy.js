/*
   Copyright

   2020, Ti Sitara/Maxwell, Martin Shishkov - gulliversoft.com

*/

var _daisy;

function w() {
	if (_daisy == undefined) {
		_daisy = new Daisy();
	}
	
	return _daisy;
}

function daisy() {
	return w();
}



var isTouchDevice = "ontouchstart" in document.documentElement ? true : false;
var BUTTON_DOWN   = isTouchDevice ? "touchstart" : "mousedown";
var BUTTON_UP     = isTouchDevice ? "touchend"   : "mouseup"


function Daisy() {}

Daisy.prototype.updateALT = function (alt, enable) {}


Daisy.prototype.ready = function (cb)
{  
	if (document.loaded)
	{
		cb();
	} 
	else
	{	
		w().readyCallback = cb;
		w().init();
	}
}

Daisy.prototype.init = function () { 
	console.log("init on demand");
	$(document).click(function() {
		$("button").effect( "highlight", "slow" );
		//$("button").effect( "bounce", "slow" );
	});
	$(document).ready(function () {
		console.log("document loaded");
		if (w().readyCallback != null)
		{
			w().readyCallback();
		} 
	});
}


Daisy.prototype.callMacro = function (macro, args, callback) {
	if (args == undefined) {
		args = "";
	}
	$.post('/macros/' + macro + "/" + args, function(data) {
		if (callback != undefined) {
			callback(macro, args, data);
		}
	});
}


Daisy.prototype.setLabel = function (id, label) {
	$("#" + id).val(label);
	$("#" + id).text(label);
}

Daisy.prototype.setClass = function (id, cssClass) {
	$("#" + id).attr("class", cssClass);
}

Daisy.prototype.createButton = function (id, label, callback, callbackUp) {
	var button = $('<button type="button" class="Default">');
	button.attr("id", id);
	button.text(label);
	if (callback != undefined) {
		button.bind(BUTTON_DOWN, callback);
	}
	if (callbackUp != undefined) {
		button.bind(BUTTON_UP, callbackUp);
	}
	return button;
}


Daisy.prototype.createMacroButton = function (id, label, macro, args) {
    var button = daisy().createButton(id, label);
    button.bind(BUTTON_DOWN, function(event) {
        daisy().callMacro(macro, args);
    });
    return button;
}
