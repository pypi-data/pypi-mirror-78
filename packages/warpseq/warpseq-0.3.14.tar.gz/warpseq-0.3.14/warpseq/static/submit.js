var NEW_ITEM = '__CREATE_NEW__';

/**********************************************************************************************************************/
/* SONG                                                                                                               */
/**********************************************************************************************************************/

// READY!


function edit_song(cb = null) {
    engine_do_edit("song",
        textboxes=["new_name", "filename"],
        selects=["scale"],
        multiple_selects=[],
        toggles=[],
        ranges=["tempo"],
    );
}

function file_new() {
    engine_post({"cmd" : "file_new"}, load_song);
}

function file_load() {
   var selectDialogueLink = $('<a href="">Select file</a>');
   var fileSelector = $('<input type="file">');
   $(fileSelector).change(function(event) {
        const reader = new FileReader();
        reader.onload = function() {
            engine_post({"cmd": "data_load", "data" : { "file_contents" : reader.result }}, load_song);
        }
        reader.readAsText(event.target.files[0]);
   });
   selectDialogueLink.click(function(){
        fileSelector.click();
        return false;
   });
   selectDialogueLink.click()
}

function file_save_as() {
   edit_song()
   var filename = document.getElementById('filename').value;
   if (filename == "") {
       filename = "warp.json";
   }
   engine_post({"cmd" : "file_save"}, function(data) {
      var filedata = JSON.stringify(data.data);
      console.log("saving")
      console.log(filedata);
      var file = new Blob([filedata], {type: 'application/json'});
      var a = document.createElement("a");
      a.href = URL.createObjectURL(file);
      a.download = filename;
      a.click();
   });
}

/**********************************************************************************************************************/
/* SCALES                                                                                                             */
/**********************************************************************************************************************/

// READY!

function load_scale_item(item) {
    load_into_workspace(SCALE, item);
}

function new_scale_item() {
    engine_do_new("scale");
}

function edit_scale(cb = null) {
    engine_do_edit("scale",
        textboxes=["new_name"],
        selects=["note","scale_type"],
        multiple_selects=["slots"],
        toggles=[],
        ranges=[],
        cb = function() { load_scales(); }
    );
}

/**********************************************************************************************************************/
/* INSTRUMENTS                                                                                                        */
/**********************************************************************************************************************/

// READY!

function load_instrument_item(item) {
    load_into_workspace(INSTRUMENT, item);
}

function new_instrument_item() {
    engine_do_new("instrument");
}

function edit_instrument(cb = null) {
    engine_do_edit("instrument",
        textboxes=["new_name"],
        selects=["device", "channel"],
        multiple_selects=[],
        toggles=["muted"],
        ranges=["min_octave","max_octave","base_octave"],
        cb = function() { load_instruments(); }
    );
}

/**********************************************************************************************************************/
/* SCENES                                                                                                             */
/**********************************************************************************************************************/

// NEXT UP!

function edit_scene(cb = null) {
    alert("NOT IMPLEMENTED!");
}

function load_scene_item(item) {
    load_into_workspace(SCENE, item);
}

function new_scene_item() {
    alert("NOT IMPLEMENTED")
}

/**********************************************************************************************************************/
/* TRACKS                                                                                                             */
/**********************************************************************************************************************/


function edit_track(cb = null) {
    alert("NOT IMPLEMENTED!");
}

function load_track_item(item) {
    load_into_workspace(TRACK, item);
}

function new_track_item() {
    alert("NOT IMPLEMENTED")
}

/**********************************************************************************************************************/
/* PATTERNS                                                                                                           */
/**********************************************************************************************************************/


function edit_pattern(cb = null) {
    alert("NOT IMPLEMENTED!");
}

function load_pattern_item(item) {
    load_into_workspace(PATTERN, item);
}

function new_pattern_item() {
    alert("NOT IMPLEMENTED")
}

/**********************************************************************************************************************/
/* TRANSFORMS                                                                                                         */
/**********************************************************************************************************************/


function edit_transform(cb = null) {
    alert("NOT IMPLEMENTED!");
}

function load_transform_item(item) {
    load_into_workspace(TRANSFORM, item);
}

function new_transform_item() {
    alert("NOT IMPLEMENTED");
}

/**********************************************************************************************************************/
/* DATA POOLS                                                                                                             */
/**********************************************************************************************************************/



function edit_data_pool(cb = null) {
    alert("NOT IMPLEMENTED!");
}

function load_data_pool_item(item) {
    load_into_workspace(DATA_POOL, item);
}

function new_data_pool_item() {
    alert("NOT IMPLEMENTED");
}

/**********************************************************************************************************************/
/* DEVICES                                                                                                             */
/**********************************************************************************************************************/


function load_device_item(item) {
    load_into_workspace(DEVICE, item);
}






