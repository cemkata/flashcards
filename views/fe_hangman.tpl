<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hangman Game</title>
    <link rel="stylesheet" href="/static/hangman/style.css">
    <script src="/static/hangman/scripts/word-list.js" defer></script>
    <script src="/static/hangman/scripts/script.js" defer></script>
</head>
<body>
<input type="hidden" id="deck" value="{{deckID}}">
<input type="hidden" id="corse" value="{{corceID}}">
    <div class="game-modal">
        <div class="content">
            <img src="#" alt="gif">
            <h4>Game Over!</h4>
            <p>The correct word was: <b>rainbow</b></p>
            <button class="play-again">Play Again</button>
        </div>
    </div>
    <div class="game-modal-loading show">
        <div class="content">
            <h4>Loading!</h4>
            <p>Please wait!</p>
        </div>
    </div>
    <div class="container">
        <div class="hangman-box">
			<img src="static/hangman/images/hangman.svg" draggable="false" alt="hangman-img">
            <h1>Hangman Game</h1>
        </div>
        <div class="game-box">
            <ul class="word-display"></ul>
            <h4 class="hint-text">Hint: <b></b></h4>
            <h4 class="guesses-text">Incorrect guesses: <b></b></h4>
            <div class="keyboard"></div>
        </div>
    </div>
</body>
</html>