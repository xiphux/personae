function addFieldRow(srcelem, container, animate) {
  var field = $(srcelem).clone();
  field.attr('id','');
  field.show();
  field.appendTo(container);
  if (animate) {
    field.highlightFade({
      speed:1000
    })
  }
}

function moveKnackClear() {
  var knackclear = $('#knackclear').clone();
  $('#knackclear').remove();
  knackclear.appendTo('#knackrows');
}

function setupDynamicTables() {
  $('#birthright0').hide();
  if ($('#birthrightsrows > tr').size() == 0) {
    addFieldRow('#birthright0','#birthrightsrows',false);
  }

  $('#weapon0').hide();
  if ($('#weapontablerows > tr').size() == 0) {
    addFieldRow('#weapon0','#weapontablerows',false);
  }

  $('#virtue0').hide();
  if ($('#virtuerows > tr').size() == 0) {
    addFieldRow('#virtue0','#virtuerows',false);
  }

  $('#boon0').hide();
  if ($('#boonrows > tr').size() == 0) {
    addFieldRow('#boon0','#boonrows',false);
  }

  $('#relic0').hide();
  if ($('#relicrows > tr').size() == 0) {
    addFieldRow('#relic0','#relicrows',false);
  }

  $('#knack0').hide();
  if ($('#knackrows > div.knackitem').size() <= 1) {
    addFieldRow('#knack0','#knackrows',false);
    moveKnackClear();
  }

  $('#art0').hide();
  if ($('#artrows > tr').size() == 0) {
    addFieldRow('#art0','#artrows',false);
  }

  $('#control0').hide();
  if ($('#controlrows > tr').size() == 0) {
    addFieldRow('#control0','#controlrows',false);
  }

}
