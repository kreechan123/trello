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
    $( ".list-container" ).each(function( index ) {
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
    $.ajax({
        url:url,
        method:'post',
        data:$(this).serialize(),
        success:function(data){
          var res = JSON.parse(data)[0]
          console.log(url);
          $("#lists").append(`
            <div class="card card-list list-container">
            <span class="list-title">${res.fields.title}</span>
                <a href="#" class="delbtn" data-id="${res.pk}" data-url="/board/${res.pk}/delete/"><span class="ui-icon ui-icon-closethick"></span></a>
            </div>`
            )
         },
     });
  });

  

  
  $(document).on('click', '.delbtn', function(e){
    e.preventDefault();
    var url = $(this).data('url');
    var elem = $(this);
    console.log('blah')
    $.ajax({
      url:url,
      method: 'get',
    }).done(function(){
      console.log("Success!");
      $(elem).parents(".card-list").remove();
    });

  });

})();
