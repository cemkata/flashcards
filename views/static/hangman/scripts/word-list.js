// Variables
var cource = document.getElementById("corse").value;
var deck = document.getElementById("deck").value;

/**http request settings*/
var xmlhttp = new XMLHttpRequest();
var url = "./getWord?courseID="+cource+"&deckID="+deck;

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        wordList = JSON.parse(this.responseText);
    }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();

var wordList = [];