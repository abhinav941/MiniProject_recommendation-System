$(document).ready(function(e){
  $('.search-panel .dropdown-menu').find('a').click(function(e) {
  e.preventDefault();
  var param = $(this).attr("href").replace("#","");
  var concept = $(this).text();
  $('.search-panel span#search_concept').text(concept);
  $('.input-group #search_param').val(param);
});
/* 1. Visualizing things on Hover - See next part for action on click */
$('#stars li').on('mouseover', function(){
  var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on
 
  // Now highlight all the stars that's not after the current hovered star
  $(this).parent().children('li.star').each(function(e){
    if (e < onStar) {
      $(this).addClass('hover');
    }
    else {
      $(this).removeClass('hover');
    }
  });
  
}).on('mouseout', function(){
  $(this).parent().children('li.star').each(function(e){
    $(this).removeClass('hover');
  });
});


/* 2. Action to perform on click */
$('#stars li').on('click', function(){
  var onStar = parseInt($(this).data('value'), 10); // The star currently selected
  var stars = $(this).parent().children('li.star');
  var val = $(this).parent().parent().parent().parent().parent().index()
  for (i = 0; i < stars.length; i++) {
    $(stars[i]).removeClass('selected');
  }

  text = $(this).parent().parent().parent().parent().find('a.article-title').text()
  
     for (i = 0; i < onStar; i++) {
      $(stars[i]).addClass('selected');
      }
      var ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
  responseMessage(ratingValue,val,text);
})


});

function responseMessage(msg,val,movie) {
$('.x'+val).fadeIn(200)
$('.x'+val).css({
  'width':'100px',
  'visibility':'visible'
}) 
$('.y'+val).hide()
$('.success-box .text-area').text(msg);
$('.success-box .movie').text(movie);
}