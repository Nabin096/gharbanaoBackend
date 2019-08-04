function showfield(name) {
  if (name == 'Other')
    document.getElementById('select-other').innerHTML = 'Other: <input type="text" name="other" />';
  else
    document.getElementById('select-other').innerHTML = '';
}