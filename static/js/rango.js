function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// add page to category functionality
$('#search_results').on('click', '.rango-add', function(e){
    e.preventDefault();
    var catid = $(this).attr("data-catid");
    var url = $(this).attr("data-url");
    var title = $(this).attr("data-title");
    var me = $(this);
    $.ajax({
        url: '/auto_add_page/',
        type: 'POST',
        data: {category_id: catid, url: url, title: title},
        dataType: 'html',
        success: function(result) {
            $('#pages').html(result);
            me.hide();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert( errorThrown )
        }
    });
});


// like functionality
$('#likes').click(function(){
    var catid = $(this).attr("data-catid");
    $.ajax({
        url: '/like/',
        type: 'POST',
        data: {category_id: catid},
        dataType: 'json',
        success: function(result) {
            $('#like_count').html(result);
            $('#likes').hide();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert( errorThrown )
        }
    });
});

// search categories
$('#suggestion').keyup(function(){
    var query = $(this).val();
    $.get('/suggest/', {search_str: query}, function(data){
        $('#cats').html(data);
    });
});


// infinite scroll support on Category page (actually up to 100 Google Search results)
$(window).scroll(function() {
    if(document.getElementById('search_results') != null &&
       // google doesn't return results more than 100
       parseInt($('#start').val()) < 100 &&
       $(window).scrollTop() == $(document).height() - $(window).height()) {

        $('.loader').show();
        // increase counter to 10 to get "next page" results
        var start = parseInt($('#start').val()) + 10;
        $('#start').val(start);
        var catid = $('#catid').val();
        var query = $('#query').val();
        $.ajax({
            url: '/search_more/',
            type: 'POST',
            data: {query: query, start: start, catid: catid},
            dataType: 'html',
            success: function(result) {
                $('.loader').hide();
                $('#search_results').append(result);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert( errorThrown );
                $('.loader').hide();
            }
        });

    }
});
