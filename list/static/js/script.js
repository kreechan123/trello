(function(){
  'use strict';

  var id = $('#lists').data('board');
  var lists_url =  `/board/${id}/lists/`;

  $.ajax({
    url: lists_url
  }).done(function(response){
    $('#lists').append(response);
    viewCards();
  });

  function viewCards() {
    $( ".card-wrapper" ).each(function( index ) {
      var elem = $(this);
      var list_id = elem.data('list-id');
      var cards_url =  `/board/${id}/lists/${list_id}/cards`;
      $.ajax({  
        url: cards_url,
      }).done(function(response) {
        elem.append(response);
      });
    });
  }

  $('#addlistform').on('submit',function(e){
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    $.ajax({
        url:url,
        method:'post',
        data:$(this).serialize(),
        success:function(data){
          var res = JSON.parse(data)[0];
          form.trigger('reset');
          var csrftoken = getCookie('csrftoken');
          var formwrap = $('.card-btn-wrapper').html();
          $("#lists").append(`
            <div class="card card-list list-container" data-list-id="${ res.pk }">
            <span class="list-title">${res.fields.title}</span>
            <div class="card-wrapper connectedSortable" data-list-id="{{ list.id }}">
        
            </div>
            <div class="dropdown">
              <button class="btn btn-sm" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fa fa-ellipsis-h" aria-hidden="true"></i>
              </button>
              <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <a class="dropdown-item" href="#">Action</a>
                  <a class="dropdown-item" href="#">Another action</a>
                  <a class="dropdown-item" href="#">Something else here</a>
                  <div class="dropdown-divider"></div>
                  <a href="#" class="delbtn dropdown-item" data-id="${res.pk}" data-url="/board/${res.pk}/delete/">
                      Archive This List
                  </a>
              </div>
            </div>
                <div class="form-base">
                  <div class="form-wrapper">
                    <form action="/board/${res.pk}/addcard/" class="card-form" method="POST">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                    <div class="card-btn-wrapper">
                  ${formwrap}
                    </div>
                    </form>
                  </div>
                </div>  
            </div>`
            )
         },
     });
  });
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

  $(document).on('shown.bs.modal', '#cardmodal', function(e){
    var elem = e.relatedTarget; // get click element
    var id = $(elem).data('id'); // get card id from the click element
    var url = $(elem).attr('href'); // defined card url: card/{card_id}/
    // console.log(e)
    $.ajax({ // ajax call get
      url:url,
    }).done(function(data){
          $('.modal-dialog').html(data);
            // dump response to specific container
      });
  });

  $(document).on('submit', '.card-form', function(e){
    var form  =  $(this);
    e.preventDefault();
    // select element that where loaded via ajax    e.preventDefault();
    var url = $(this).attr('action');
    var cardwrap = $(this).parents('.list-container').find('.card-wrapper');
    $.ajax({
        url:url,
        method:'post',
        data:$(this).serialize(),
     }).done(function(data){
          var res = JSON.parse(data)[0]
          form.trigger('reset');
          cardwrap.append(
            `<div class="card-each-wrap">
              	<a href="/card/${res.pk}/detail/" class="class-card" data-id="${res.pk}" data-toggle="modal" data-target="#cardmodal">${res.fields.title}</a>
              	<a href="/card/${res.pk}/delete/" class="card-delete" data-id=${res.pk}><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a>
            </div>`
          )
     })
  });
  $(document).on('click', '.card-delete', function(e){
  	e.preventDefault();
  	var url = $(this).attr('href');
  	var elem = $(this);
  	$.ajax({
  		url: url,
  		method: 'get',
  	}).done(function(){
  		$(elem).parents('.card-each-wrap').remove();
  	});
  });

$(document).on('focusout', 'span.list-title', function(e){
  e.preventDefault();
  var elem = $(this);
  var text = $(this).text();
  var old = $(this).data('title');
  if (text.length === 0){
    $(this).text(old);
    console.log(text);
    return false;
  }
  var id = $(this).parents('.card-list').data('list-id');
  var url = $(this).data('url');
  var csrf = $(this).attr('csrf');
  console.log(csrf);
  $.ajax({
    url: url,
    method: 'post',
    data: {'title': text, 'csrfmiddlewaretoken': csrf},
  }).done(function(response){
    elem.data('title', response.title);
  });
})
  
  $(document).on('click', '.delbtn', function(e){
    // select element that where loaded via ajax
    e.preventDefault();
    var url = $(this).data('url');
    var elem = $(this);
    $.ajax({
      url:url,
      method: 'get',
    }).done(function(){
      $(elem).parents(".card-list").remove();
    });

  });

})();
