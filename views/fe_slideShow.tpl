% include('__header.tpl')
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel='stylesheet' href='./static/flashcard.css'>
</head>
<html>
   <body>
<input type="hidden" id="deck" value="{{deckID}}">
<input type="hidden" id="corse" value="{{corceID}}">

<div class="slideshow-container">

<div class="mySlides fade">
  <div id="numSlides" class="numbertext"></div>
  </br>
    <div class="centerThis">
		<div class="scene scene--card">
		  <div class="card">
			<div id="front" class="card__face card__face--front">front</div>
			<div id="back" class="card__face card__face--back">back</div>
		  </div>
		</div>
	</div>
</div>

<a class="prev" onclick="plusSlides(-1)">&#10094;</a>
<a class="next" onclick="plusSlides(1)">&#10095;</a>

<br>

<div id="allDots" style="text-align:center">
</div>
</div>

<script src="./static/flashcard.js"></script>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
   </body>
</html>
% include('__footer.tpl')