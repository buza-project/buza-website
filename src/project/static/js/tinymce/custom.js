tinymce.init({
  selector: 'textarea',
  height: 100,
  menubar: false,
  plugins: [
    // XXX (Pi): Comment out plugins not available with django-tinymce's bundled copy.
    'advlist',
    'autolink',
    'lists',
    // 'link',
    // 'image',
    // 'charmap',
    'print',
    'preview',
    // 'anchor',
    // 'textcolor',
    'searchreplace',
    'visualblocks',
    // 'code',
    'fullscreen',
    'insertdatetime',
    'media',
    'table',
    'contextmenu',
    'paste',
    // 'code',
    // 'help',
    'wordcount'
  ].join(','),  // TinyMCE 3 wants a comma-separated string list.
  toolbar: 'insert | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});
