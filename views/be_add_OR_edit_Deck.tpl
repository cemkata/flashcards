% include('__header.tpl')
% if defined('error_str'):
<link rel='stylesheet' href='/static/1b-icon.css'>
% end
</head>
<body>
<h3>Deck</h3>
<div>

% if defined('error_str'):
    <div class="bar error">
      <i class="ico">&#9747;</i> {{error_str}}
    </div>
	<br><br>
% end

% if defined('deckName'):
<form action="./updateDeck" method="post">
% else:
<form action="./addDeck" method="post">
% end

	<label for="course_id">Deck name:</label><label style="color:red">*</label>
% if defined('deckName'):
	<input type="text" id="deckName" name="deckName" value="{{deckName}}">
% else:
	<input type="text" id="deckName" name="deckName" required>
% end


% if defined('did'):
	<input type="hidden" id="did" name="did" value="{{did}}">
% end

% if defined('cid'):
	<input type="hidden" id="course_id" name="course_id" value="{{cid}}">
% end
	<input type="submit" value="Submit">
</form>
</div>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
</body>
</html>
% include('__footer.tpl')