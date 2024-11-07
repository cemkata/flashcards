% include('__header.tpl')
<script>
function confirmEdit(did, cid) {
	window.location.href = './editDeck?courseID=' + cid + '&deckID=' + did;
}
function confirmDelete(did, cid) {
	if (confirm('Are you sure you want to delete this deck?')) {
	  window.location.href = './deleteDeck?courseID=' + cid + '&deckID=' + did;
	} 
}
</script>
</head>
<html>
   <body>
	<h3>Select deck editor</h3>
<div>
<table class="pretyPrint">
  <tr>
    <th>Deck name</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>
  <tr>
    <td colspan="3"><input type="button" onclick="location.href='./showCards?courseID={{course_id}}&deckID={{deck[0]['id']}}';" value="Cards in deck - {{course_name}} by: {{deck[0]['info']}}" /></td>
  </tr>
% for i in range(1, len(deck)):
  <tr>
    <td><input type="button" onclick="location.href='./showCards?courseID={{course_id}}&deckID={{deck[i]['id']}}';" value="Cards in deck - {{course_name}} by: {{deck[i]['info']}}" /></td>
    <td><input type="button" onclick="confirmEdit('{{deck[i]['id']}}', '{{course_id}}')" value="Edit" /></td>
    <td><input type="button" onclick="confirmDelete('{{deck[i]['id']}}', '{{course_id}}')"value="Delete"/></td>
  </tr>
% end
</table>
</div>
<input type="button" onclick="location.href='./editDeck?courseID={{course_id}}&deckID=-1';" value="Add new deck" />
<input type="button" id = "backButton" onclick="window.history.back();" value="Back" />
   </body>
</html>
% include('__footer.tpl')