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

function delete_scale(item, name) {
    engine_delete(SCALE, item, name);
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

function delete_instrument(item, name) {
    engine_delete(INSTRUMENT, item, name);
}

/**********************************************************************************************************************/
/* SCENES                                                                                                             */
/**********************************************************************************************************************/

function edit_scene(cb = null) {
    engine_do_edit(SCENE,
        textboxes=["new_name"],
        selects=["scale"],
        multiple_selects=[],
        toggles=["auto_advance"],
        ranges=["rate"],
        cb = function() { load_scenes(); }
    );
}

function load_scene_item(item) {
    load_into_workspace(SCENE, item);
}

function new_scene_item() {
   engine_do_new(SCENE);
}

function shift_scene_up(item) {
    engine_reorder(SCENE, item, -1);
}

function shift_scene_down(item) {
    engine_reorder(SCENE, item, 1);
}

function delete_scene(item, name) {
    engine_delete(SCENE, item, name);
}

function play_scene(item) {
    console.log("NOT IMPLEMENTED")
}

/**********************************************************************************************************************/
/* TRACKS                                                                                                             */
/**********************************************************************************************************************/

function edit_track(cb = null) {
    engine_do_edit(TRACK,
        textboxes=["new_name"],
        selects=["instrument_mode"],
        multiple_selects=["instruments"],
        toggles=["muted"],
        ranges=[],
        cb = function() { load_tracks(); }
    );
}

function load_track_item(item) {
    load_into_workspace(TRACK, item);
}

function new_track_item() {
   engine_do_new(TRACK);
}

function shift_track_up(item) {
    engine_reorder(TRACK, item, -1);
}

function shift_track_down(item) {
    engine_reorder(TRACK, item, 1);
}

function delete_track(item, name) {
    engine_delete(TRACK, item, name);
}

/**********************************************************************************************************************/
/* PATTERNS                                                                                                           */
/**********************************************************************************************************************/


function edit_pattern(cb = null) {
   engine_do_edit(PATTERN,
        textboxes=["new_name", "rate"],
        selects=["scale","direction","pattern_type","audition_with"],
        multiple_selects=[],
        toggles=[],
        ranges=["octave_shift"],
        cb = function() { load_patterns(); }
    );
}

function load_pattern_item(item) {
    load_into_workspace(PATTERN, item);
}

function new_pattern_item() {
    engine_do_new(PATTERN);
}

function delete_pattern(item, name) {
   engine_delete(PATTERN, item, name);
}

function update_grid_backend(original_cmd, category, gridOptions) {

    var postback = original_cmd + "_postback";

    console.log("grid update:" + postback);
    // iterate through every node in the grid
    var results = [];
    gridOptions.api.forEachNode(function(rowNode, index) {
        results.push(rowNode.data);
    });
    console.log("data");
    console.log(results);
    engine_post({
         "cmd" : postback,
         "id" : document.getElementById("obj_id").value,
         "data" : results
    }, function(ok_data) {
        console.log("its all good");
        generic_grid_init(original_cmd, category);
    });
}

function generic_grid_init(cmd, category) {

   var obj_id = document.getElementById("obj_id").value;
   engine_post({
       "cmd" : cmd,
       "id" : obj_id,
       "data" : { "category" : category }
   }, function(data) {

        console.log("grid data")
        console.log(data);

       // FIXME: this needs event handlers to send back changes

       var columnDefs = data["data"]["column_defs"];
       var rowData = data["data"]["row_data"];
       var gridDiv = document.querySelector('#myGrid');

       columnDefs[0]["rowDrag"] = function(params) {
           return !params.node.group;
       };

       gridDiv.innerHTML = '';

       function keyDownListener(e) {
           // delete the rows
           // keyCode 8 is Backspace
           // keyCode 46 is Delete
           if (e.keyCode === 8 || e.keyCode === 46) {
               const sel = gridOptions.api.getSelectedRows();
               gridOptions.api.applyTransaction({remove: sel});
           }
       }


       var gridOptions = {
           columnDefs: columnDefs,
           rowData: rowData,
           editType: 'fullRow',
           singleClickEdit: true,
           stopEditingWhenGridLosesFocus: true,
           rowDragManaged: true,
           enableMultiRowDragging: true,
           rowSelection: 'multiple',
           rowDeselection: true,
           animateRows: true,
           onGridReady: (params) => {
               document.addEventListener('keydown', keyDownListener);
           },
           onCellEditingStopped: function(event) { console.log('cell editing stopped'); console.log(event); update_grid_backend(cmd, category, gridOptions); },
           onCellValueChanged: function(event) { console.log('cell editing stopped'); console.log(event); update_grid_backend(cmd, category, gridOptions); },
           onRowDragEnd: function(event) { console.log('on row drag end'); console.log(event); update_grid_backend(cmd, category, gridOptions); }
       };

       new agGrid.Grid(gridDiv, gridOptions);

       $('#new_row_button').on('click', function() {
           gridOptions.api.applyTransaction({ add: [{}] });
       });

   });
}

function load_pattern_grid(category) {
    edit_pattern();
    generic_grid_init('grid_for_pattern', category);
}

function load_pattern_common_grid() {
    load_pattern_grid('common');
}

function load_pattern_pitch_grid() {
   load_pattern_grid('pitch');
}

function load_pattern_time_grid() {
   load_pattern_grid('time');
}

function load_pattern_modulation_grid() {
   load_pattern_grid('modulation');
}

function load_pattern_control_grid() {
   load_pattern_grid('control');
}

function audition_pattern() {
    var obj_id = document.getElementById("obj_id").value;
    engine_post({
       "cmd" : "audition_pattern",
       "id" : obj_id
   }, null);
}

/**********************************************************************************************************************/
/* TRANSFORMS                                                                                                         */
/**********************************************************************************************************************/


function edit_transform(cb = null) {
   engine_do_edit(TRANSFORM,
        textboxes=["new_name"],
        selects=["divide","direction","applies_to","audition_instrument","audition_pattern"],
        multiple_selects=[],
        toggles=["auto_reset","arp"],
        ranges=[],
        cb = function() { load_transforms(); }
    );
}

function load_transform_item(item) {
    load_into_workspace(TRANSFORM, item);
}

function new_transform_item() {
    engine_do_new(TRANSFORM);
}

function delete_transform(item, name) {
   engine_delete(TRANSFORM, item, name);
}

function audition_transform() {
    var obj_id = document.getElementById("obj_id").value;
    engine_post({
       "cmd" : "audition_transform",
       "id" : obj_id
   }, null);
}

/**********************************************************************************************************************/
/* DATA POOLS                                                                                                             */
/**********************************************************************************************************************/



function edit_data_pool(cb = null) {
   engine_do_edit(TRANSFORM,
        textboxes=["new_name"],
        selects=[],
        multiple_selects=[],
        toggles=[],
        ranges=[],
        cb = function() { load_data_pools(); }
    );
}

function load_data_pool_item(item) {
    load_into_workspace(DATA_POOL, item);
}

function new_data_pool_item() {
    engine_do_new(DATA_POOL);
}

function delete_data_pool(item, name) {
    engine_delete(DATA_POOL, item, name);
}

/**********************************************************************************************************************/
/* DEVICES                                                                                                             */
/**********************************************************************************************************************/


function load_device_item(item) {
    load_into_workspace(DEVICE, item);
}






