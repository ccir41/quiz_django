$(function () {
  /*======================================================
                        Message fade out     
    =======================================================*/
  $(".alert-auto-dismiss")
    .delay(2000)
    .slideUp(500, function () {
      $(this).alert("close");
    });
});
