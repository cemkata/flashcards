var cards;

const ver = 2.6;

// Variables
var cource = document.getElementById("corse").value;
var deck = document.getElementById("deck").value;
var flashCardFront = document.getElementById("front");
var flashCardBack = document.getElementById("back");
var numSlides = document.getElementById("numSlides");
var dots = document.getElementsByClassName("dot");
var allDots = document.getElementById("allDots");
var card = document.querySelector('.card');
var slideIndex = 1;
const transitionDuration = parseInt(getComputedStyle(card).transition.split(" ")[1]);
var transitionFlag = false;


/**http request settings*/
var xmlhttp = new XMLHttpRequest();
var url = "./getDeck?courseID="+cource+"&deckID="+deck;

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        cards = JSON.parse(this.responseText);
		
		cards = shuffle(cards)

        for(let i = 1; i <= cards.length; i++){
            allDots.innerHTML += `<span class="dot" onclick="currentSlide(`+ i +`)"></span>`;
        }

        numSlides.innerText = "1 / " + cards.length;
        showSlides(slideIndex);

        card.addEventListener( 'click', function() {
          card.classList.toggle('is-flipped');
        });

        document.addEventListener('keydown', function (event) {
          event.preventDefault();
          if (event.key === 'ArrowLeft') {
            plusSlides(-1);
          }
          if (event.key === 'ArrowRight') {
            plusSlides(1);
          }
          if (event.key === ' ') {
            card.classList.toggle('is-flipped');
          }
        });

    }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  if(transitionFlag){return}
  if (n > cards.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = cards.length}
  for (var i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  card.classList.toggle('is-flipped', false);
  transitionFlag = true;
  flashCardFront.innerHTML = cards[slideIndex - 1].front;
  timer = setTimeout(function(){
      flashCardBack.innerHTML = cards[slideIndex - 1].back;
      transitionFlag = false;
  }, transitionDuration * 1000);
  
  numSlides.innerText = slideIndex + " / " + cards.length;
  dots[slideIndex-1].className += " active";
}

function shuffle(array) {
	let currentIndex = array.length,  randomIndex;

	// While there remain elements to shuffle...
	while (currentIndex != 0) {

	  // Pick a remaining element...
	  randomIndex = Math.floor(Math.random() * currentIndex);
	  currentIndex--;

	  // And swap it with the current element.
	  [array[currentIndex], array[randomIndex]] = [
		array[randomIndex], array[currentIndex]];
	}

	return array;
}
