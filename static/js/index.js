function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var API_URL = 'pattern';
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    headers: {"X-CSRFToken": csrftoken}
});


function get_pattern_post(query) {
    $.ajax({
        type: "POST",
        url: API_URL,
        data: JSON.stringify({text: query}),
        dataType: 'json',
        success: renderPatternResult, 
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            console.log("Status: " + textStatus); 
            console.log("Error: " + errorThrown); 
        } 
    });
}

function onKey(e) {
    var text = $("#search").text().trim();
    if (text) {
        get_pattern_post(text);
    }
}

function renderPatternResult(data) {
    var htmlFrag = '';
    data.patterns.forEach(function(pattern) {
        htmlFrag += '<p class="pattern">' + pattern.text + ' <font size="3" color="green">' + pattern.count + '</font></p>';
        htmlFrag += '<p class="example">';
        pattern.colls.forEach(function(ngram) {
            htmlFrag += '<p class="example">';
            ngram.examples.slice(0, 1).forEach(function(example) {
                var content = example.text.replace(/\[/g, '<font class="main">').replace(/\]/g, '</font>');
                htmlFrag += '<font class="prev">' + content + '</font>';
                htmlFrag += '<font class="count">' + example.count + '</font>';
            });
            htmlFrag += '</p>';
        });
        htmlFrag += '</p>';
    });
    $('.pattern-area').html(htmlFrag);
}