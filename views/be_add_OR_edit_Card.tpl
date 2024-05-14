% include('__header.tpl')
</head>
<body>
<h3>Flashcard</h3>
<div>
% if defined('question'):
<form action="./updateCard" method="post">
% else:
<form action="./addCard" method="post">
% end
	<label for="question">Question:</label><label style="color:red">*</label>
% if defined('question'):
	<textarea id="question" name="question" rows="8" cols="50" required>{{question}}</textarea>
% else:
	<textarea id="question" name="question" rows="8" cols="50" required></textarea>
% end
	<label for="answer">Answer:</label><label style="color:red">*</label>
% if defined('answer'):
	<textarea id="answer" name="answer" rows="8" cols="50" required>{{answer}}</textarea>
% else:
	<textarea id="answer" name="answer" rows="8" cols="50" required></textarea>
% end
	<label for="answer">Select course:</label><label style="color:red">*</label>
	<select name="course_id" id="course_id" required>
	<option value="">Select course</option>
	% for c in courses:
		<option value="{{c.course_id}}">{{c.name}}</option>
	% end
	</select>
% if defined('qid'):
	  <input type="hidden" id="qid" name="qid" value="{{qid}}">
% end
	  <input type="submit" value="Submit">
</form>
</div>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
</body>
</html>
% include('__footer.tpl')