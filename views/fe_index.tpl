% include('__header.tpl')
</head>
<html>
   <body>
	<h3>Select corse</h3>
<div>
	% for c in courses:
		<input type="button" onclick="location.href='./showcourse?courseID={{c.course_id}}';" value="{{c.name}}" />
	% end
</div>
   </body>
</html>
% include('__footer.tpl')