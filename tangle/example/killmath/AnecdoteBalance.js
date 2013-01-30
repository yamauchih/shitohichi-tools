//
//  AnecdoteBalance.js
//  KillMath
//
//  Created by Bret Victor on 4/15/11.
//  (c) 2011 Bret Victor.  MIT open-source license.
//

(function(){

var AnecdoteBalance = this.AnecdoteBalance = new Class({

	initialize: function (canvas) {
		this.canvas = this.element = canvas;
		
		this.width = parseInt(canvas.get("width"));
		this.height = parseInt(canvas.get("height"));
		this.ctx = this.canvas.getContext("2d");
		
		this.dx = 0;
		this.animationTime = 0;
		
		this.leftPlot = new Plot();
		this.leftPlot.func = function (t) { return t * t; };

		this.rightPlot = new Plot();
		this.rightPlot.func = function (t) { return Math.exp(-t); };
		this.rightPlot.x = 160;
		
		this.beam = new Beam(this);
		
		this.animationInterval = this.updateAnimation.periodical(20, this);
	},
	
	updateAnimation: function () {
		var now = Date.now();
		var dt = 0.001 * (now - (this.lastTimestamp || now));
		this.lastTimestamp = now;
		if (dt === 0) { return; }
		
		this.animationTime += dt;
		if (this.animationTime > 8) {
			this.animationTime = 0;
			this.dx = 0;
			this.beam.x = 0;
		}
		
		var dy = this.rightPlot.yForX(this.beam.x) - this.leftPlot.yForX(this.beam.x);
		this.dx += -3.5 * dy * dt;
		this.dx *= 0.985 * Math.exp(-dt);
		
		this.beam.x += this.dx * dt;

		this.drawInContext(this.ctx);
	},
	
	drawInContext: function (ctx) {
		ctx.fillStyle = "#fff";
		ctx.fillRect(0,0,this.width,this.height);
		
		this.leftPlot.drawInContext(ctx);
		this.rightPlot.drawInContext(ctx);
		this.beam.drawInContext(ctx);
	}
});


var Beam = new Class({
	
	initialize: function (balance) {
		this.balance = balance;
		this.x = 0;
		this.height = 100;
		
		this.trayLeft = new Image();
		this.trayLeft.src = "Images/BalanceTrayLeft.png";
		this.trayRight = new Image();
		this.trayRight.src = "Images/BalanceTrayRight.png";
		this.trayWidth = 36;
		this.trayHeight = 39;
		
		this.tLabel = new Image();
		this.tLabel.src = "Images/BalanceTLabel.png";
		this.tLabelWidth = 20;
		this.tLabelHeight = 11;
	},
	
	drawInContext: function (ctx) {
		ctx.fillStyle = "#333";
		ctx.strokeStyle = "#333";
		ctx.lineWidth = 5;
		
		var x1 = this.balance.leftPlot.x + this.x;
		var y1 = this.balance.leftPlot.y + this.balance.leftPlot.yForX(this.x);
		var x2 = this.balance.rightPlot.x + this.x;
		var y2 = this.balance.rightPlot.y + this.balance.rightPlot.yForX(this.x);

		var pivotX = 0.5 * (x1 + x2);
		var pivotY = y1 + (pivotX - x1) * (y2 - y1) / (x2 - x1);
		
		ctx.beginPath();
		ctx.moveTo(x1, y1);
		ctx.lineTo(x2, y2)
		ctx.stroke();
		ctx.closePath();

		ctx.beginPath();
		ctx.moveTo(pivotX, pivotY);
		ctx.lineTo(pivotX - 5, this.height)
		ctx.lineTo(pivotX + 5, this.height)
		ctx.closePath();
		ctx.fill();
		
		if (this.trayLeft.complete) {
			ctx.drawImage(this.trayLeft, x1 - 0.5 * this.trayWidth, y1);
		}
		if (this.trayRight.complete) {
			ctx.drawImage(this.trayRight, x2 - 0.5 * this.trayWidth, y2);
		}
		if (this.tLabel.complete) {
			ctx.drawImage(this.tLabel, pivotX - this.tLabelWidth, this.height + 2);
			ctx.font = "13px Times New Roman";
			var text = "" + (this.x / this.balance.leftPlot.width).round(2);
			if (text.length < 4) { text += "0"; }
			ctx.fillText(text, pivotX + 2, this.height + 12);
		}
	}

});


var Plot = new Class({

	initialize: function () {
		this.x = 0;
		this.y = 0;
		this.width = 70;
		this.height = 100;
	},
	
	yForX: function (x) {
		return this.height * (1 - this.func(x / this.width));
	},

	drawInContext: function (ctx) {
		ctx.fillStyle = "#ddd";
		ctx.beginPath();
		ctx.moveTo(this.x, this.y + this.height);

		for (var x = 0; x < this.width; x++) {
			ctx.lineTo(this.x + x, this.y + this.yForX(x));
		}
		
		ctx.lineTo(this.x + this.width, this.y + this.height);
		ctx.closePath();
		ctx.fill();
	}
	
});


})();
