% include('__header.tpl')
</head>
<html>
   <body>
	<h3>Home</h3>
<div>
	<input type="button" onclick="location.href='./newCard';" value="Add Card" />
	<input type="button" onclick="location.href='./newcourse';" value="Add course" />
	<input type="button" onclick="location.href='./showcourses';" value="Show courses" />
<form action="./showCards" method="get">
	<select name="courseID" id="courseID" required>
	<option value="">Select course</option>
	% for c in courses:
		<option value="{{c.course_id}}">{{c.name}}</option>
	% end
	</select>
	  <input type="submit" value="Show Cards">
</form>
</div>
   </body>
</html>
% include('__footer.tpl')