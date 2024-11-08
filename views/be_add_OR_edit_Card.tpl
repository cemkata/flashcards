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
	<select name="course_id" id="course_id" required onchange="fillDeckDropDown(this)">
	<option value="">Select course</option>
	% for c in courses:
		<option value="{{c.course_id}}">{{c.name}}</option>
	% end
	</select>
	<label for="deck">Deck:</label>
	<select name="deck_id" id="deck_id">
		<option value="">Default deck</option>
	</select>
% if defined('qid'):
	  <input type="hidden" id="qid" name="qid" value="{{qid}}">
% end
	  <input type="submit" value="Submit">
</form>
</div>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
<script>
	function fillDeckDropDown(selc) {
		const xhr = new XMLHttpRequest();
		xhr.open("GET", "./getDecks?courseID="+selc.value, true);

		// Send the proper header information along with the request
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

		xhr.onreadystatechange = () => {
		  // Call a function when the state changes.
		  if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
			// Request finished. Do processing here.
			var myArr = JSON.parse(xhr.responseText);
			var newSelect=document.getElementById('deck_id');
			newSelect.replaceChildren() 

			for(let i = 0; i < myArr.length; i++){
			   var opt = document.createElement("option");
			   opt.value= myArr[i].id;
			   opt.innerHTML = myArr[i].info; // whatever property it has

			   // then append it to the select element
			   newSelect.appendChild(opt);
			}

		  }
		};
		xhr.send();
	}
</script>
</body>
</html>
% include('__footer.tpl')
