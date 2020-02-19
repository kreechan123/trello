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
          $("#lists").append(`
            <div class="card card-list">
              <div class="card-header contenteditable-hd" style="height: initial;">
                ${res.fields.title}
              </div>
              <div class="card-body card-list"> 
              </div> 
            </div>`
            )
         },
     });
  });


  $('.navbar').on('click', function(){
    console.log('card clicked')
  });


  
  $(document).on('click', '.www', function(e){
    e.preventDefault();
    console.log('card clicked');
    var elem = $(this);
    console.log(elem.data('list-id'));

  });



  

})();
