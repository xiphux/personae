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

function setupDotWidgets(type) {
  var widgetclass = ''
  var dotemptyclass = '';
  var dotfullclass = '';
  var dotempty = '';
  var dotfull = '';
  if (type == "dot") {
    widgetclass = 'dotwidget';
    dotemptyclass = 'dotempty';
    dotfullclass = 'dotfull';
    dotempty = '&#9678;';
    dotfull = '&#9673;';
  } else if (type == "square") {
    widgetclass = 'squarewidget';
    dotemptyclass = 'squareempty';
    dotfullclass = 'squarefull';
    dotempty = '&#9634;';
    dotfull = '&#9635;';
  } else {
    return false;
  }
  $("select." + widgetclass).each(function() {
    var spanelement = document.createElement('span');
    var span = jQuery(spanelement);
    var count = $(this).children('option').size();
    var selectedval = ($(this).val() * 1);
    var spanstr = '';
    for (var idx = 1; idx < count; idx++) {
      var dotelem = document.createElement('span');
      var dot = jQuery(dotelem);
      if (idx <= selectedval) {
        dot.append(dotfull).addClass(dotfullclass);
      } else {
        dot.append(dotempty).addClass(dotemptyclass);
      }
      spanstr += dot.context.outerHTML;
    }
    var hiddenvalueelement = document.createElement('input');
    var hiddenvalue = jQuery(hiddenvalueelement);
    hiddenvalue.attr('name', $(this).attr('name')).attr('type', 'hidden').val(selectedval);
    spanstr += hiddenvalue.context.outerHTML
    span.append(spanstr).addClass(widgetclass);
    $(this).replaceWith(span.context.outerHTML);
  });
}

function setupDotWidgetEvents(type) {
  var widgetclass = ''
  if (type == "dot") {
    widgetclass = 'dotwidget';
  } else if (type == "square") {
    widgetclass = 'squarewidget';
  } else {
    return false;
  }
  var dotwidgets = $("span." + widgetclass)
  dotwidgets.live("mouseout", function(e) {
    var emptyclass = 'dotempty';
    var fullclass = 'dotfull';
    var emptycontent = '&#9678;';
    var fullcontent = '&#9673;';
    var dotgroup = $(e.target).parent();
    if (dotgroup.hasClass('squarewidget')) {
      emptyclass = 'squareempty';
      fullclass = 'squarefull';
      emptycontent = '&#9634;';
      fullcontent = '&#9635;';
    }
    var dots = dotgroup.children('span');
    var count = dots.size();
    var val = (dotgroup.children('input').val() * 1);
    for (var idx = 0; idx < count; idx++) {
      var curdot = dots.eq(idx);
      if (idx < val) {
        if (curdot.hasClass(emptyclass)) {
          curdot.html(fullcontent).removeClass(emptyclass).addClass(fullclass);
        }
      } else {
        if (curdot.hasClass(fullclass)) {
          curdot.html(emptycontent).removeClass(fullclass).addClass(emptyclass);
        }
      }
    }
  });
  dotwidgets.live("click", function(e) {
    var dotgroup = $(e.target).parent()
    var valelem = dotgroup.children('input');
    var newval = $(e.target).prevAll('span').size() + 1;
    var currentval = (valelem.val() * 1);
    if ((newval == 1) && (currentval == 1)) {
      valelem.val(0);
    } else {
      valelem.val(newval);
    }
    dotgroup.highlightFade({
      speed:200
    });
  });
  $("span." + widgetclass + " > span").live("mouseover", function(e) {
    var emptyclass = 'dotempty';
    var fullclass = 'dotfull';
    var emptycontent = '&#9678;';
    var fullcontent = '&#9673;';
    var dot = $(e.target);
    if (dot.parent().hasClass('squarewidget')) {
      emptyclass = 'squareempty';
      fullclass = 'squarefull';
      emptycontent = '&#9634;';
      fullcontent = '&#9635;';
    }
    if (dot.hasClass(emptyclass)) {
      dot.html(fullcontent).removeClass(emptyclass).addClass(fullclass);
    }
    dot.prevAll('span.' + emptyclass).html(fullcontent).removeClass(emptyclass).addClass(fullclass);
    dot.nextAll('span.' + fullclass).html(emptycontent).removeClass(fullclass).addClass(emptyclass);
  });
}
