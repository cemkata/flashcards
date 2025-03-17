% include('__header.tpl')
</head>
<html>
   <body>
	<h3>Select corse (flashcards)</h3>
<div>
	% for c in courses:
		<input type="button" onclick="location.href='./showcourse?courseID={{c.course_id}}';" value="{{c.name}}" />
	% end
</div>
	<h3>Select corse (hangman)</h3>
<div>
	% for c in courses:
		<input type="button" onclick="location.href='./showhangman?courseID={{c.course_id}}';" value="{{c.name}}" />
	% end
</div>
   </body>
</html>
% include('__footer.tpl')