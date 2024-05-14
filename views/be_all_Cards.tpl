% include('__header.tpl')
<script>
function confirmEdit(qid) {
	window.location.href = './editCard?id=' + qid;
}
function confirmDelete(qid) {
	if (confirm('Are you sure you want to delete this question?')) {
	  window.location.href = './deleteCard?id=' + qid;
	} 
}
</script>


</head>
<body>

<h3>Flash cards for {{c_name}}</h3>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />

<div>
<table class="pretyPrint">
  <tr>
    <th>Course ID</th>
    <th>Question</th>
    <th>Answer</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>

% for fc in flashCards:
  <tr>
    <td>{{fc.course_id}}</td>
    <td style="word-break:break-all;">
    % for q in fc.question.split("\n"):
      {{q}}
      </br>
    % end
    </td>

    <td style="word-break:break-all;">
    % for a in fc.answer.split("\n"):
      {{a}}
      </br>
    % end
    </td>

    <td><input type="button" onclick="confirmEdit({{fc.qid}})" value="Edit" /></td>
    <td><input type="button" onclick="confirmDelete({{fc.qid}})"value="Delete"/></td>
  </tr>
% end

</table>
</div>
</body>
</html>
% include('__footer.tpl')