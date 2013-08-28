function submitForm(form) {
    url=form["url"].value;
    xmlhttp=XMLHttpRequest();
    xmlhttp.open("POST","/",false);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(url);
    window.location.reload();
}

function getDetails(id) {
    $.getJSON('/jobs/' + id, function(data) {
       output=data.stdout;
       $(details).html(output).wrap('<pre />')
    })
}

$.getJSON('/jobs', function(data) {
    output='<form method="post">'
    output+='<input type="text" name="url"'
    output+='onkeydown="if (event.keyCode == 13) { submitForm(this.form); return false; }">'
    output+='<input type="button" value="Add" onclick="submitForm(this.form)">'
    output+='</form>'
    output+="<table><th align='left'>Job</th><th align='right'>Status</th>"
    for (var i in data) {
        output+="<tr>"
        output+="<td><a href=javascript:getDetails("+i+")>"
        output+=data[i].name + "</a></td>"
        output+="<td align='right'>" + data[i].status + "</td>"
        output+="</tr>"
    }
    output+="</table>"
    $(jobs).html(output);
})
