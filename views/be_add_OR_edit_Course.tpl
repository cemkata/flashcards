% include('__header.tpl')
% if defined('error_str'):
<link rel='stylesheet' href='/static/1b-icon.css'>
% end
</head>
<body>
<h3>Course</h3>
<div>

% if defined('error_str'):
    <div class="bar error">
      <i class="ico">&#9747;</i> {{error_str}}
    </div>
	<br><br>
% end

% if defined('cid'):
<form action="./updatecourse" method="post">
% else:
<form action="./addcourse" method="post">
% end
	<label for="course_id">Course id:</label><label style="color:red">*</label>
% if defined('course_id'):
	<input type="number" id="course_id" name="course_id" value="{{course_id}}" readonly>
% else:
	<input type="number" id="course_id" name="course_id" required>
% end
	<br><br>
	<label for="name">Name:</label><label style="color:red">*</label>
% if defined('name'):
	<input type="text" id="name" name="name" value="{{name}}" required>
% else:
	<input type="text" id="name" name="name" required>
% end
	<br><br>
	<label for="description">Description:</label>
% if defined('description'):
	<textarea id="description" name="description" rows="8" cols="50">{{description}}</textarea>
% else:
	<textarea id="description" name="description" rows="8" cols="50"></textarea>
% end

% if defined('cid'):
	<input type="hidden" id="cid" name="cid" value="{{cid}}">
% end
	<input type="submit" value="Submit">
</form>
</div>
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
</body>
</html>
% include('__footer.tpl')