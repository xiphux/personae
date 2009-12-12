var menuY = null;

function setupFloatingNav(clonesrc, floatingdest, widthsrc) {
  var nav = $(clonesrc);
  var floatingnav = $(floatingdest);

  menuY = nav.position().top;

  floatingnav.hide();
  floatingnav.append(nav.clone().html());

  $(window).scroll(function(){
    var windowY = $(document).scrollTop();
    var floatingnav = $(floatingdest);
    if (windowY > menuY) {
      var nav = $(widthsrc);
      var navwidth = nav.width();
      var floatingwidth = floatingnav.width();
      floatingnav.show();
      if (navwidth != floatingwidth) {
        floatingnav.width(navwidth);
      }
    } else {
      floatingnav.hide();
    }
  });
}
