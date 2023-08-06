define(['base/js/namespace'], function(Jupyter){
    Jupyter._target = '_self';
});

$('#new_notebook').hide();
$('#open_notebook').hide();
$('#copy_notebook').hide();
$('#rename_notebook').hide();
$('#save_checkpoint').hide();
$('#restore_checkpoint').hide();
$('#kill_and_exit').hide();
$('#trust_notebook').hide();
$('#file_menu .divider').each(function(i, el) { $(el).hide(); });
$('#login_widget').hide();
$('#kernel_menu .divider').hide();
$('#menu-change-kernel').hide();

if (window.location.pathname == '/terminals/1') {
  $('#header-container img').hide();
  $('a[title="dashboard"]').attr('onclick', 'window.history.back(); return false');
  $('a[title="dashboard"]').removeAttr('href');
  $('a[title="dashboard"]').prepend('<span>Notebook</span>');
  $('a[title="dashboard"]').prepend('<i class="fa fa-angle-left" />');
  $('a[title="dashboard"]').addClass('notebook-back-link');
  $('#header-container').append('<span class="terminal-span">Terminal</span>');
  $('#header-container').addClass('notebook-back-header');
  $('#header-container').show();
} else {
  // Disable a link back to the tree view
  $('#header-container').hide();
  $('a[title="dashboard"]').attr('href', '#');
}
$('a[title="dashboard"]').attr('target', '_self');
$('a[title="dashboard"]').attr('title', 'notebook');

window.setTimeout(function() {
  $("#notebook_name").off();
  require(['base/js/events'], function(events) {
    events.on('set_dirty.Notebook', function(evt, data) {
      window.parent.postMessage({text: 'mark_dirty', dirty: data.value}, '*');
    })
  });
}, 1200);

