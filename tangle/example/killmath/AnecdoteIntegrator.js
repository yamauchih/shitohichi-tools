//
//  AnecdoteIntegrator.js
//  KillMath
//
//  Created by Bret Victor on 4/14/11.
//  (c) 2011 Bret Victor.  MIT open-source license.
//

(function(){

var AnecdoteIntegrator = this.AnecdoteIntegrator = new Class({

	initialize: function (canvas) {
		this.canvas = this.element = canvas;
		
		this.width = parseInt(canvas.get("width"));
		this.height = parseInt(canvas.get("height"));
		this.ctx = this.canvas.getContext("2d");
		
		this.topPlot = new TopPlot();
		this.bottomPlot = new BottomPlot();
		this.tank = new Tank();
		
		this.initialRevealedWidth = -65;
		this.revealedWidth = this.initialRevealedWidth;
		
		this.animationInterval = this.updateAnimation.periodical(20, this);
	},
	
	updateAnimation: function () {
		var now = Date.now();
		var dt = 0.001 * (now - (this.lastTimestamp || now));
		this.lastTimestamp = now;
		if (dt === 0) { return; }
		
		this.revealedWidth += 40 * dt;
		
		this.topPlot.revealedWidth = this.revealedWidth;
		this.bottomPlot.revealedWidth = this.revealedWidth;
		this.tank.x = this.revealedWidth - 0.5 * this.tank.width;
		this.tank.waterHeight = this.bottomPlot.valueForX(this.revealedWidth);
		this.tank.opacity = (1 - (this.revealedWidth - this.topPlot.width) / 20).limit(0,1);
		
		this.topPlot.updateWithTimeInterval(dt);
		
		this.drawInContext(this.ctx);
		
		if (this.revealedWidth > this.topPlot.width + 100) {
			this.revealedWidth = this.initialRevealedWidth;
			this.topPlot.reset();
		}
	},
	
	drawInContext: function (ctx) {
		ctx.fillStyle = "#fff";
		ctx.fillRect(0,0,this.width,this.height);
		
		this.topPlot.drawInContext(ctx);
		this.tank.drawBackgroundInContext(ctx);
		this.tank.drawFillInContext(ctx);
		this.bottomPlot.drawInContext(ctx);
	}

});


var TopPlot = new Class({

	initialize: function () {
		this.x = 0;
		this.y = 0;
		this.width = 300;
		this.height = 70;
		this.revealedWidth = 0;
		
		this.stripes = [];
		for (var x = 0; x < this.width; ) {
			var stripe = new Stripe(this,x);
			this.stripes.push(stripe);
			x += stripe.width;
		}
	},

	valueForX: function (x) {
		return Math.sin(x / this.width * Math.PI) * this.height;
	},

	reset: function (dt) {
		for (var i = 0; i < this.stripes.length; i++) { this.stripes[i].reset(); }
	},

	updateWithTimeInterval: function (dt) {
		for (var i = 0; i < this.stripes.length; i++) { this.stripes[i].updateWithTimeInterval(dt); }
	},
	
	drawInContext: function (ctx) {
		for (var i = 0; i < this.stripes.length; i++) { this.stripes[i].drawInContext(ctx); }
	}
	
});


var Stripe = new Class({

	initialize: function (plot, x) {
		this.plot = plot;
		this.x = x;

		this.width = 1;
		this.height = this.plot.valueForX(this.x);
		this.initialY = this.plot.height - this.height;

		this.reset();
	},

	reset: function () {
		this.y = this.initialY;
		this.dy = 0;
		this.isDropping = false;
	},
	
	updateWithTimeInterval: function (dt) {
		if (this.isDropping) {
			this.dy += 800 * dt;
			this.y += this.dy * dt;
		}
		else if (this.plot.revealedWidth >= this.x - 22) {
			this.isDropping = true;
		}
	},
	
	drawInContext: function (ctx) {
		ctx.fillStyle = "#ddd";
		ctx.fillRect(this.plot.x + this.x, this.plot.y + this.initialY, this.width, this.height);
		ctx.fillStyle = "#6ee6f1";
		ctx.fillRect(this.plot.x + this.x, this.plot.y + this.y, this.width, this.height);
	}
});


var Tank = new Class({

	initialize: function () {
		this.x = 0;
		this.y = 92;
		this.width = 20;
		this.height = 78;
		this.waterHeight = 0;
		this.opacity = 1;
		
		this.imageWidth = 26;
		this.imageHeight = 78;
		
		this.backgroundImage = new Image();
		this.backgroundImage.src = "Images/IntegratorVial.png"

		this.fillImage = new Image();
		this.fillImage.src = "Images/IntegratorVialFill.png"
	},
	
	drawBackgroundInContext: function (ctx) {
		if (!this.backgroundImage.complete) { return; }
		if (this.opacity <= 0) { return; }
		ctx.drawImage(this.backgroundImage,this.x + 5,this.y);
	},
	
	drawFillInContext: function (ctx) {
		if (!this.fillImage.complete) { return; }
		if (this.waterHeight <= 0) { return; }
		if (this.opacity <= 0) { return; }

		ctx.drawImage(this.fillImage, 0,               this.imageHeight - this.waterHeight, 26, this.waterHeight, 
	                                  this.x + 5, this.y + this.imageHeight - this.waterHeight, 26, this.waterHeight);
		if (this.opacity < 1) {
			ctx.fillStyle = "rgba(255,255,255," + (1 - this.opacity) + ")";
			ctx.fillRect(this.x + 5, this.y, this.imageWidth, this.imageHeight);
		}
	}
	
});

var BottomPlot = new Class({

	initialize: function () {
		this.x = 0;
		this.y = 100;
		this.width = 300;
		this.height = 70;
	},
	
	valueForX: function (x) {
		return 0.5 * this.height * (1.0 - Math.cos(x / this.width * Math.PI));
	},
	
	drawInContext: function (ctx) {
		ctx.fillStyle = "#ddd";
		var plotWidth = Math.min(this.revealedWidth - 4, this.width);
		if (plotWidth <= 0) { return; }
		
		ctx.beginPath();
		ctx.moveTo(this.x, this.y + this.height);

		for (var x = 0; x < plotWidth; x++) {
			var y = this.valueForX(x);
			ctx.lineTo(this.x + x, this.y + this.height - y);
		}
		
		ctx.lineTo(this.x + plotWidth, this.y + this.height);
		ctx.closePath();
		ctx.fill();
	}
	
});

})();

