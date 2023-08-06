const SWITCHER_DIV = 'nav1'
const NAV_DIV = 'nav2';
const WORKSPACE_DIV = 'workspace';

const SONG = 'song';
const DEVICE = 'device';
const INSTRUMENT = 'instrument';
const SCALE = 'scale';
const SCENE = 'scene';
const TRACK = 'track';
const PATTERN = 'pattern';
const TRANSFORM = 'transform';
const DATA_POOL = 'data_pool';
const GRID = 'grid';

/**********************************************************************************************************************/
/* general  utilities                                                                                                 */
/**********************************************************************************************************************/

function engine_post(data, on_success, jsonify=true) {

    console.log("engine_post")
    console.log(data)

    if (on_success == null) {
        on_success = function(data) {}
    }

    if (jsonify) {
        data = JSON.stringify(data)
    }

    $.ajax({
        type: 'POST',
        url: '/engine',
        data: data,
        dataType: 'json',
        contentType: "application/json",
        cache: false,
        success: function(data) {
            console.log(data);
            on_success(data)
        },
        error: function(data) {
            console.log("ERROR: " + data)
            console.log(data);
            //flash_error(data.responseJSON['msg']);
        }
    });

}

function load_into_div(url, div) {

    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'text',
        cache: false,
        success: function(data) {
            $("#" + div).html(data);
        },
        error: function(data) {
            console.log(data);
            try {
                flash_error(data.responseJSON['msg']);
            } catch(err) {
                console.log(err);
                console.log("communication with server failed");
            }
        }
    });

}

function engine_reorder(category, item, direction) {
   engine_post({
       "cmd" : "reorder_" + category,
       "data" : { "id" : item, "direction" : direction }
   }, null);
   load_into_nav(category);
}

function engine_delete(category, item, name) {

   var r = confirm("Delete " + name + " ?");

   if (r == false) {
      return;
   }

   engine_post({ "cmd" : "delete_" + category, "id" : item }, null);

   load_into_nav(category);
}

function engine_do_edit(category, textboxes=[], selects=[], multiple_selects=[], toggles=[], ranges=[], cb=null) {
   if (cb == null) {
       cb = function(data) {}
   }
   var data = {};
   var key = "";
   //console.log("---------------------------------------");
   //console.log("engine do edit: " + category);
   if (category != 'song') {
      data["id"] = document.getElementById("obj_id").value;
   }
   for(i=0; i<textboxes.length; i++) {
       key = textboxes[i];
       //console.log("key= " + key);
       value = document.getElementById(key).value;
       //console.log(value);
       data[key] = value;
   }
   for(i=0; i<selects.length; i++) {
       key = selects[i];
       //console.log("select = " + key);
       value = null_if_dash(select2_get_selection(key));
       //console.log(value);
       data[key] = value;
   }
   for(i=0; i<multiple_selects.length; i++) {
       key = multiple_selects[i];
       //console.log("key= " + key);
       value = null_if_empty(select2_get_selections(key));
       //console.log(value);
       data[key] = value;
   }
   for(i=0; i<toggles.length; i++) {
       key = toggles[i];
       //console.log("key= " + key);
       value = document.getElementById(key).checked;
       //console.log(value);
       data[key] = value;
   }
   console.log(data);
   for(i=0; i<ranges.length; i++) {
       key = ranges[i];
       //console.log("key= " + key);
       value = document.getElementById(key).value;
       //console.log(value);
       data[key] = value;
   }
   //console.log("final data?")
   //console.log(data);
   //console.log("edit_" + category);
   //console.log(data);
   engine_post({
       "cmd" : "edit_" + category,
       "data" : data
   }, cb);
}

function engine_do_new(category) {

    engine_post({
        "cmd" : "new_" + category,
        "data" : {}
    }, function(data) {
        console.log(data)
        load_into_nav(category);
        load_into_workspace(category, data.data);
    });
}

/**********************************************************************************************************************/
/* page specifics                                                                                                     */
/**********************************************************************************************************************/

function clear_slots() {
   $('#slots').val(null).trigger('change');
}
function clear_scale_type() {
   $('#scale_type').val(null).trigger('change');
}

/**********************************************************************************************************************/
/* populates the first nav widget dynamically                                                                         */
/**********************************************************************************************************************/

function load_into_switcher() {
   load_into_div("/pages/switcher/1", SWITCHER_DIV);
}

/**********************************************************************************************************************/
/* clicking on the first nav menu loads something into the second nav menu                                            */
/**********************************************************************************************************************/

function load_into_nav(category) {
    load_into_div("/pages/" + category + "/list", NAV_DIV);
}

/**********************************************************************************************************************/
/* clicking on the second nav menu loads something into the workspace                                                 */
/**********************************************************************************************************************/

function load_into_workspace(category, item) {
    load_into_div("/pages/" + category + "/" + item, WORKSPACE_DIV);
    if ((category != 'song') && (category != 'grid')) {
        toggle_nav2(item);
    }
}

function toggle_nav2(item) {
    $(".nav2_item").removeClass("nav2_item_active");
    $(".nav2_item").addClass("nav2_item_inactive");
    if (item == -1) {
        return;
    }
    $("#nav2_item_" + item).removeClass("nav2_item_inactive");
    $("#nav2_item_" + item).addClass("nav2_item_active");
}

/**********************************************************************************************************************/
/* first nav menu                                                                                                     */
/**********************************************************************************************************************/

function load_song(data)    {   load_into_nav(SONG); load_into_workspace(SONG, 0, 0) }
function load_instruments() {   load_into_nav(INSTRUMENT);       }
function load_devices()     {   load_into_nav(DEVICE);           }
function load_scales()      {   load_into_nav(SCALE);            }
function load_scenes()      {   load_into_nav(SCENE);            }
function load_tracks()      {   load_into_nav(TRACK);            }
function load_patterns()    {   load_into_nav(PATTERN);          }
function load_transforms()  {   load_into_nav(TRANSFORM);        }
function load_data_pools()  {   load_into_nav(DATA_POOL);        }
function load_grid()        {   load_into_workspace(GRID, 0, 0); }

/**********************************************************************************************************************/
/* startup page                                                                                                       */
/**********************************************************************************************************************/

function load_initial_ui_state(data) {
    load_into_switcher();
    load_into_nav(SONG);
    load_grid();
}

/**********************************************************************************************************************/
/* WORKSPACE DIALOGS                                                                                                  */
/**********************************************************************************************************************/

function select2_get_selection(element) {
    data = $("#"+element).select2('data');
    for(var index in data) {
        if (data[index].selected) {
            console.log("select2_get_selection => " + data[index].text)
            return data[index].text;
        }
    }
    return null;
}

function select2_get_selections(element) {
    var results = [];
    data = $("#"+element).select2('data')
    console.log("DATA")
    console.log(data)
    for(var index in data) {
        if (data[index].selected) {
            console.log("pushing: " + data[index].text);
            results.push(data[index].text);
        }
    }
    return results;
}

function select2_activate(field) {
    var element = $("#" + field)
    element.select2({
        width: 200
    });
    element.on('select2:select', function (e) {
        if (intercept_field(field, select2_get_selection(field))) {
           edit_this();
        }
    });
}

function textbox_activate(field) {
    $("#" + field).focusout(function(){
         if (intercept_field(field, $("#" + field).value)) { edit_this(); }
    });
    document.getElementById(field).addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            if (intercept_field(field, $("#" + field).value)) { edit_this(); }
        }
    });
}

function range_activate(field) {
  var elem = $("#" + field);
  document.getElementById(field).addEventListener("input", () => {
      $("#" + field + "_value").text(elem[0].value);
      edit_this();
  });
}

function toggle_activate(field) {
    document.getElementById(field).addEventListener('change', (event) => {
        edit_this();
    });
}

function null_if_dash(item) {
   if (item == "-") {
      return null;
   }
   return item;
}

function null_if_empty(alist) {
   if (alist.length == 0) {
       return null;
   }
   return alist
}

function close_workspace() {
   $(".nav2_item").removeClass("nav2_item_active");
   load_grid();
}

/**********************************************************************************************************************/
/* FLASH MESSAGES                                                                                                     */
/**********************************************************************************************************************/

function flash_msg(msg) {
   console.log("msg: " + msg);
   $("#flash").removeClass("flash_error");
   $("#flash").addClass("flash_happy");
   $("#flash").html(msg);
}

function flash_error(msg) {
   console.log("error: " + msg);
   $("#flash").removeClass("flash_happy");
   $("#flash").addClass("flash_error");
   $("#flash").html(msg);
}


/**********************************************************************************************************************/

function global_play() {
    engine_post({
       "cmd" : "global_play"
   }, null);
}

function global_stop() {
    engine_post({
       "cmd" : "global_stop"
   }, null);
}

function midi_panic() {
    engine_post({
       "cmd" : "midi_panic"
   }, null);
}


/**********************************************************************************************************************/
/* GO!                                                                                                                */
/**********************************************************************************************************************/

$(document).ready(function() {
    console.log("warp engines online");
    load_initial_ui_state();
    console.log("take us out");
});
