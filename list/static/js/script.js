$(document).ready(function() {
    $('#MyModal').on('click', function(){
      $('#MyModal').modal('show');
    });
    $('.contenteditable').on('focusout', function(){
      var x = $(this).html();
      console.log(x);
    });
    // $('#addlist').on('click', function(){
    //     $('.addhdn').toggle('hide')
        
    // })
  }) //doc.ready closing tag