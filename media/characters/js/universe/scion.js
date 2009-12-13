function addBirthright(animate) {
  var id = document.getElementById("birthrightid").value;
  id = (id * 1) + 1;
  var field = $('#birthright0').clone();
  field.attr('id','birthright' + id);
  field.show();
  field.appendTo("#birthrightsrows");
  if (animate) {
    $("#birthright" + id).highlightFade({
      speed:1000
    });
  }
  document.getElementById("birthrightid").value = id.toString();
  setupDotWidgets("dot");
}

function addWeapon(animate) {
  var id = document.getElementById("weaponid").value;
  id = (id * 1) + 1;
  var field = $('#weapon0').clone();
  field.attr('id','weapon' + id);
  field.show();
  field.appendTo('#weapontablerows');
  if (animate) {
    $("#weapon" + id).highlightFade({
      speed:1000
    })
  }
  document.getElementById("weaponid").value = id.toString();
}

function addVirtue(animate) {
  var id = document.getElementById("virtueid").value;
  id = (id * 1) + 1;
  var field = $('#virtue0').clone();
  field.attr('id','virtue' + id);
  field.show();
  field.appendTo('#virtuerows');
  if (animate) {
    $("#virtue" + id).highlightFade({
      speed:1000
    })
  }
  document.getElementById("virtueid").value = id.toString();
}

function addBoon(animate) {
  var id = document.getElementById("boonid").value;
  id = (id * 1) + 1;
  var field = $('#boon0').clone();
  field.attr('id','boon' + id);
  field.show();
  field.appendTo('#boonrows');
  if (animate) {
    $("#boon" + id).highlightFade({
      speed:1000
    })
  }
  document.getElementById("boonid").value = id.toString();
}

function addRelic(animate) {
  var id = document.getElementById("relicid").value;
  id = (id * 1) + 1;
  var field = $('#relic0').clone();
  field.attr('id','relic' + id);
  field.show();
  field.appendTo('#relicrows');
  if (animate) {
    $("#relic" + id).highlightFade({
      speed:1000
    })
  }
  document.getElementById("relicid").value = id.toString();
}

function addKnack(animate) {
  var id = document.getElementById("knackid").value;
  id = (id * 1) + 1;
  var field = $('#knack0').clone();
  field.attr('id','knack' + id);
  field.show();
  var knackclear = $('#knackclear').clone();
  $('#knackclear').remove();
  field.appendTo('#knackrows');
  knackclear.appendTo('#knackrows');
  if (animate) {
    $("#knack" + id).highlightFade({
      speed:1000
    })
  }
  document.getElementById("knackid").value = id.toString();
}

function setupDynamicTables() {
  $('#birthright0').hide();
  if (document.getElementById("birthrightid").value == 0) {
    addBirthright(false);
    //$("#birthright1 > .removerow").hide();
  }

  $('#weapon0').hide();
  if (document.getElementById("weaponid").value == 0) {
    addWeapon(false);
    //$("#weapon1 > .removerow").hide();
  }

  $('#virtue0').hide();
  if (document.getElementById("virtueid").value == 0) {
    addVirtue(false);
    //$("#virtue1 > .removerow").hide();
  }

  $('#boon0').hide();
  if (document.getElementById("boonid").value == 0) {
    addBoon(false);
    //$("#boon1 > .removerow").hide();
  }

  $('#relic0').hide();
  if (document.getElementById("relicid").value == 0) {
    addRelic(false);
    //$("#relic1 > .removerow").hide();
  }

  $('#knack0').hide();
  if (document.getElementById("knackid").value == 0) {
    addKnack(false);
    //$("#knack1 > .removerow").hide();
  }

}
