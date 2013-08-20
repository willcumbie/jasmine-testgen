import sublime, sublime_plugin
import os

class OpenJasmineSpecCommand(sublime_plugin.WindowCommand):
  def run(self, paths = [], name = ""):
    current_dir = self.window.active_view().file_name()
    if current_dir:
      self.go_to_spec(current_dir)
    else:
      sublime.error_message("No file open in active view.")

  def go_to_spec(self, directory):
    dirs = directory.split("/")
    dirs.insert(dirs.index("ck"), "spec")
    filename_with_spec = dirs[-1].split(".")[0] + "_spec.js"
    dirs[-1] = filename_with_spec
    new_path = "/".join(dirs)

    file_exists = os.path.exists(new_path)

    if file_exists:
      sublime.active_window().open_file(new_path)
    else:
      old_view = self.window.active_view()
      new_view = self.window.new_file()
      new_view.set_name(new_path)
      self.create_spec(old_view, new_view)

  def create_spec(self, old_view, new_view):
    first_line = old_view.find("^goog\\.provide\\('.*?'\\);$", 0);
    class_name = old_view.substr(first_line).split("'")[1]

    snippet = """goog.require('$1');

describe ('$1', function () {

  var testObj;

  beforeEach(function () {
    testObj = new $1();
  });

});
"""
    edit = new_view.begin_edit()
    template_text = snippet.replace("$1", class_name)
    new_view.insert(edit, 0, template_text)
    new_view.end_edit(edit)

