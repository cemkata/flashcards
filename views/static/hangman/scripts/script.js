const wordDisplay = document.querySelector(".word-display");
const guessesText = document.querySelector(".guesses-text b");
const keyboardDiv = document.querySelector(".keyboard");
const hangmanImage = document.querySelector(".hangman-box img");
const gameModal = document.querySelector(".game-modal");
const gameModalLoading = document.querySelector(".game-modal-loading");

const playAgainBtn = gameModal.querySelector("button");

const caseInsensitive = true;

var keyboardTimeout = false;

// Initializing game variables
let currentWord, correctLetters, wrongGuessCount;
const maxGuesses = 9;

const resetGame = () => {
    // Ressetting game variables and UI elements
    correctLetters = [];
    wrongGuessCount = 0;
    hangmanImage.src = "static/hangman/images/hangman-0.svg";
    guessesText.innerText = `${wrongGuessCount} / ${maxGuesses}`;
    wordDisplay.innerHTML = currentWord.split("").map(() => `<li class="letter"></li>`).join("");
    keyboardDiv.querySelectorAll("button").forEach(btn => btn.disabled = false);
    gameModal.classList.remove("show");

    //Show all chars that are not in the defined alphabet
    let nonAlpabetChars = []
    if(caseInsensitive){
        nonAlpabetChars = [...new Set(currentWord.toLowerCase())];
    }else{
        nonAlpabetChars = [...new Set(currentWord)];
    }
    let tmpButton = {};
    tmpButton.disabled = true;
    for(let i = 0; i < nonAlpabetChars.length; i++){
        if(!alphabet.includes(nonAlpabetChars[i])){
            initGame(tmpButton, nonAlpabetChars[i]);
        }
    }

    //remove the space
    initGame(alphabetButtons[alphabetButtons.length - 1], ' ');
}

const getRandomWord = () => {
    // Selecting a random word and hint from the wordList
    const { word, hint } = wordList[Math.floor(Math.random() * wordList.length)];
    currentWord = word; // Making currentWord as random word
    document.querySelector(".hint-text b").innerText = hint;
    resetGame();
}

const gameOver = (isVictory) => {
    // After game complete.. showing modal with relevant details
    const modalText = isVictory ? `You found the word:` : 'The correct word was:';
    gameModal.querySelector("img").src = `static/hangman/images/${isVictory ? 'victory' : 'lost'}.gif`;
    gameModal.querySelector("h4").innerText = isVictory ? 'Congrats!' : 'Game Over!';
    gameModal.querySelector("p").innerHTML = `${modalText} <b>${currentWord}</b>`;
    gameModal.classList.add("show");
}

const initGame = (button, clickedLetter) => {
    // Checking if clickedLetter is exist on the currentWord
    if(currentWord.includes(clickedLetter) || (caseInsensitive && currentWord.includes(clickedLetter.toUpperCase()))) {
        // Showing all correct letters on the word display
        [...currentWord].forEach((letter, index) => {
            if(letter === clickedLetter || (caseInsensitive && letter === clickedLetter.toUpperCase())){
                correctLetters.push(letter);
                wordDisplay.querySelectorAll("li")[index].innerText = letter;
                wordDisplay.querySelectorAll("li")[index].classList.add("guessed");
            }
        });
    } else {
        // If clicked letter doesn't exist then update the wrongGuessCount and hangman image
        wrongGuessCount++;
        hangmanImage.src = `static/hangman/images/hangman-${wrongGuessCount}.svg`;
    }
    button.disabled = true; // Disabling the clicked button so user can't click again
    guessesText.innerText = `${wrongGuessCount} / ${maxGuesses}`;

    // Calling gameOver function if any of these condition meets
    if(wrongGuessCount === maxGuesses) return gameOver(false);
    if(correctLetters.length === currentWord.length) return gameOver(true);
}

// Creating keyboard buttons and adding event listeners
// The sapce " " should be last button added.
const alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
      'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
      't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü', 'ß', ' '];

for (let i = 0; i < alphabet.length; i++) {
    const button = document.createElement("button");
    button.innerText = alphabet[i];
    keyboardDiv.appendChild(button);
    button.addEventListener("click", (e) => initGame(e.target, alphabet[i]));
}

const alphabetButtons = keyboardDiv.getElementsByTagName("button");
alphabetButtons[alphabetButtons.length - 1].style.display = 'none'; //Hide the sapce " ".

const getWordFromServer = () => {
    if (wordList.length != 0)
    {
        gameModalLoading.classList.remove("show");
        getRandomWord();
        playAgainBtn.addEventListener("click", getRandomWord);
    }else{
        var myTimeout = setTimeout(getWordFromServer, 1000);
    }
}

getWordFromServer();

document.onkeydown = function(evt) {
    if(keyboardTimeout){return}
    keyboardTimeout = true;
    for(var i = 0; i < alphabet.length; i++){
      if(evt.key.toLowerCase() == alphabet[i] && !alphabetButtons[i].disabled){
          initGame(alphabetButtons[i], alphabet[i]);
          break;
      }
    }
    setTimeout(() => {
      keyboardTimeout = false;
    }, 200); //wait a 0.2 seconds before processing other key
};
