% include('__header.tpl')
</head>
<html>
   <body>
	<h3>Select deck</h3>
<div>
	% for d in deck:
		<input type="button" onclick="location.href='./showflashcards?courseID={{course_id}}&deckID={{d['id']}}';" value="{{course_name}} by: {{d['info']}}" />
	% end
</div>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
   </body>
</html>
% include('__footer.tpl')