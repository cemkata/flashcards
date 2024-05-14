% include('__header.tpl')
<script>
function confirmEdit(qid) {
	window.location.href = './editcourse?id=' + qid;
}
function confirmDelete(qid) {
	if (confirm('Are you sure you want to delete this question?')) {
	  window.location.href = './deletecourse?id=' + qid;
	} 
}
</script>


</head>
<body>

<h3>Courses</h3>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />

<div>
<table class="pretyPrint">
  <tr>
    <th>Course ID</th>
    <th>Name</th>
    <th>Description</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>

% for fc in coursesList:
  <tr>
    <td>{{fc.course_id}}</td>
    <td>{{fc.name}}</td>
    <td>{{fc.description}}</td>
    <td><input type="button" onclick="confirmEdit({{fc.id}})" value="Edit" /></td>
    <td><input type="button" onclick="confirmDelete({{fc.id}})"value="Delete"/></td>
  </tr>
% end

</table>
</div>
</body>
</html>
% include('__footer.tpl')