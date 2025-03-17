% include('__header.tpl')
</head>
<html>
   <body>
		% if defined('hangman'):
	<h3>Select hangman category</h3>
		%else:
	<h3>Select deck</h3>
		% end
<div>
	% for d in deck:
		% if defined('hangman'):
		<input type="button" onclick="location.href='./showhangmanwordselection?courseID={{course_id}}&deckID={{d['id']}}';" value="{{course_name}} by: {{d['info']}}" />
		%else:
		<input type="button" onclick="location.href='./showflashcards?courseID={{course_id}}&deckID={{d['id']}}';" value="{{course_name}} by: {{d['info']}}" />
		% end
	% end
</div>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
   </body>
</html>
% include('__footer.tpl')