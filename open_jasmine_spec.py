import sublime, sublime_plugin
import os
from functools import partial

spec_view_list = []

class OpenJasmineSpecCommand(sublime_plugin.WindowCommand ):

  def run(self, paths = [], name = ""):
    current_dir = self.window.active_view().file_name()
    if current_dir:
      self.go_to_spec(current_dir)
    else:
      sublime.error_message("No file open in active view.")

  def go_to_spec(self, directory):
    dirs = [directory]
    while (os.path.split(dirs[0])[0] and os.path.split(dirs[0])[1]):
      new_sections = os.path.split(dirs[0])
      dirs = [new_sections[0], new_sections[1]] + dirs[1:]
    dirs.insert(dirs.index("ck"), "spec")

    filename_with_spec = dirs[-1].split(".")[0] + "_spec.js"
    dirs[-1] = filename_with_spec

    new_path = os.path.join(*dirs)
    new_dir = os.path.join(*dirs[0:-1])

    file_exists = os.path.exists(new_path)
    dir_exists = os.path.exists(new_dir)

    if file_exists:
      sublime.active_window().open_file(new_path)
    else:
      if not dir_exists:
        self.create_directory(*dirs[0:-1])
      old_view = self.window.active_view()
      new_file = open(new_path, 'w')
      new_file.close();

      new_view = sublime.active_window().open_file(new_path)
      new_view.settings().set('jasmine_closure_new_spec', True)

      first_line = old_view.find("^goog\\.provide\\('.*?'\\);$", 0)
      class_name = old_view.substr(first_line).split("'")[1]
      new_view.settings().set('jasmine_closure_class_name', class_name)

  def create_directory(self, *folders):
    path_so_far = ""
    for folder in folders:
      path_so_far = os.path.join(path_so_far, folder)
      if not os.path.exists(path_so_far):
        os.mkdir(path_so_far)

class JasmineSpecOpenListener (sublime_plugin.EventListener):
  def on_load(self, view):
    if (view.settings().get('jasmine_closure_new_spec')):
      self.create_spec(view)
      view.settings().set('jasmine_closure_new_spec', False)

  def create_spec(self, view):

    snippet = """goog.require('$1');

describe ('$1', function () {
  var testObj;

  beforeEach(function () {
    testObj = new $1();
  });
});
"""
    edit = view.begin_edit()
    class_name = view.settings().get('jasmine_closure_class_name')
    template_text = snippet.replace("$1", class_name)
    view.insert(edit, 0, template_text)
    view.end_edit(edit)

    handler = partial(self.add_test, view)
    view.window().show_input_panel('Enter statement for test (enter nothing to quit):', '', handler, None, None)

  def add_test(self, view, text):
    test_label = text.strip()
    if (test_label != ''):
      test_template = """

  it("$1", function () {
  });"""
      test_text = test_template.replace("$1", test_label)

      edit = view.begin_edit()
      test_end = view.find_all('\}\);', 0)[-1].begin()
      view.insert(edit, test_end - 1, test_text)

      handler = partial(self.add_test, view)
      view.window().show_input_panel('Enter statement for test (enter nothing to quit):', '', handler, None, None)
