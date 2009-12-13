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
    var pendingclass = 'dotpending';
    var emptycontent = '&#9678;';
    var fullcontent = '&#9673;';
    var dotgroup = $(e.target).parent();
    if (dotgroup.hasClass('squarewidget')) {
      emptyclass = 'squareempty';
      fullclass = 'squarefull';
      pendingclass = 'squarepending';
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
    dots.removeClass(pendingclass);
  });
  dotwidgets.live("click", function(e) {
    var dotgroup = $(e.target).parent()
 
    var emptyclass = 'dotempty';
    var fullclass = 'dotfull';
    var pendingclass = 'dotpending';
    var emptycontent = '&#9678;';
    var fullcontent = '&#9673;';
    if (dotgroup.hasClass('squarewidget')) {
      emptyclass = 'squareempty';
      fullclass = 'squarefull';
      pendingclass = 'squarepending';
      emptycontent = '&#9634;';
      fullcontent = '&#9635;';
    }

    var valelem = dotgroup.children('input');
    var newval = $(e.target).prevAll('span').size() + 1;
    var currentval = (valelem.val() * 1);
    if ((newval == 1) && (currentval == 1)) {
      newval = 0;
    }
    valelem.val(newval);
    var dots = dotgroup.children('span');
    var count = dots.size();
    dots.removeClass(pendingclass);
    for (var idx = 0; idx < count; idx++) {
      var curdot = dots.eq(idx);
      if ((idx < newval) || ((idx == 0) && (newval == 0))) {
        if (curdot.hasClass(emptyclass)) {
          curdot.html(fullcontent).removeClass(emptyclass).addClass(fullclass);
        }
      } else {
        if (curdot.hasClass(fullclass)) {
          curdot.html(emptycontent).removeClass(fullclass).addClass(emptyclass);
        }
      }
      if ((idx == 0) && (newval < 2)) {
        curdot.addClass(pendingclass);
      }
    }
  });
  $("span." + widgetclass + " > span").live("mouseover", function(e) {
    var emptyclass = 'dotempty';
    var fullclass = 'dotfull';
    var pendingclass = 'dotpending';
    var emptycontent = '&#9678;';
    var fullcontent = '&#9673;';
    var dot = $(e.target);
    if (dot.parent().hasClass('squarewidget')) {
      emptyclass = 'squareempty';
      fullclass = 'squarefull';
      pendingclass = 'squarepending';
      emptycontent = '&#9634;';
      fullcontent = '&#9635;';
    }

    var currentval = (dot.siblings('input').val() * 1);
    var currentdot = dot.prevAll('span').size() + 1;
    var dotgroup = dot.parent();
    var dots = dotgroup.children('span');
    var count = dots.size();

    var solidval = 0;
    var pendingval = 0;
    if (currentval < currentdot) {
      solidval = currentval;
      pendingval = currentdot;
    } else {
      solidval = currentdot;
      pendingval = currentval;
    }

    for (var idx = 0; idx < count; idx++) {
      var idxdot = dots.eq(idx);
      if (idx < pendingval) {
        if (idxdot.hasClass(emptyclass)) {
          idxdot.html(fullcontent).removeClass(emptyclass).addClass(fullclass);
        }
      } else {
        if (idxdot.hasClass(fullclass)) {
          idxdot.html(emptycontent).removeClass(fullclass).addClass(emptyclass);
        }
      }

      if ((currentval == 1) && (currentdot == 1) && (idx == 0)) {
        if (!(idxdot.hasClass(pendingclass))) {
          idxdot.addClass(pendingclass);
        }
      } else if (idx < solidval) {
        if (idxdot.hasClass(pendingclass)) {
          idxdot.removeClass(pendingclass);
        }
      } else if (idx < pendingval) {
        if (!(idxdot.hasClass(pendingclass))) {
          idxdot.addClass(pendingclass);
        }
      } else {
        if (idxdot.hasClass(pendingclass)) {
          idxdot.removeClass(pendingclass);
        }
      }
    }
  });
}
