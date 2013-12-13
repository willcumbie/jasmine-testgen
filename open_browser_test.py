import sublime, sublime_plugin
import webbrowser

spec_view_list = []

class OpenBrowserTest(sublime_plugin.WindowCommand ):

  def run(self, paths = [], name = ""):
    current_dir = self.window.active_view().file_name()
    if current_dir:
      self.open_test(current_dir)
    else:
      sublime.error_message("No file open in active view.")

  def open_test(self, target):
    target_url = "http://localhost:5100/run_tests?path=/ck/" + target.rsplit('/ck/', 1)[1]
    webbrowser.open(target_url, new=0, autoraise=True)
