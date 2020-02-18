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
      console.log(elem.data('list-id'));
      var list_id = elem.data('list-id');
      var cards_url =  `/board/${id}/lists/${list_id}/cards`;
      //  console.log(list_id);
      $.ajax({  
        url: cards_url,
      }).done(function(response) {
        $('#cards').append(response);
      });
    });
  }

  // var elem = $(this);
  // console.log(elem.data('list-id'));

})();


