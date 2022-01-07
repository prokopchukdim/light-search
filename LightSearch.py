import sublime
import sublime_plugin
import webbrowser


class LightSearch():
	#Loads settings and current engine
	def __init__(self):
		self.settings = sublime.load_settings('LightSearch.sublime-settings')
		self.current_engine = self.settings.get('engine', 'google')

	#changes current engine to eng
	def change_engine(self, eng:str):
		self.current_engine = eng
		self.settings.set('engine', eng)

	#returns current engine
	def get_engine(self):
		return self.current_engine

	#returns start of link for current engine
	def get_search_link(self, eng:str):
		return self.settings.get('engine_links')[eng]

#Sublime TextInputHandler that handles inputs for SearchCommand  
class QueryInputHandler(sublime_plugin.TextInputHandler):

	def __init__(self, current_view):
		self.view = current_view

	#If the user has a string highlighted, returns the user's highlighted string.
	def initial_text(self):
		to_return = ''
		#For each slected region in view, check if empty. If there is a selection, process it and return it as a placeholder.
		for reg in self.view.sel():
			if reg.empty():
				return ""
			else:
				part = self.view.substr(reg).strip()
				to_return += part
		if len(to_return) >= 1:
			return to_return
		else:
			return ""
	
	def placeholder(self):
		return 'Enter message to search'

	#User has exited command prompt or deleted an already entered arg
	def cancel(self):
		pass

#Sublime ListInputHandler that handles inputs for ChangeEngineCommand
class EngineInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			('Google', 'google'),
			('StackOverflow', 'stack'),
			('DuckDuckGo', 'duck'),
			('Bing', 'bing'),
			('Yahoo', 'yahoo')
		]

#Controls the SearchCommand command call
class LightSearchCommand(sublime_plugin.TextCommand):
	
	def run(self,edit,query):
		webbrowser.open(LightSearch.get_search_link(LightSearch.get_engine()) + query)

	def input(self, args):
		if 'query' not in args:
			return QueryInputHandler(self.view)

	def input_description(self):
		return "String to search"

#Controls the ChangeEngineCommand command call
class LightSearchChangeEngineCommand(sublime_plugin.TextCommand):
	
	def run(self,edit,engine):
		LightSearch.change_engine(engine)

	def input(self, args):
		return EngineInputHandler()

	def input_description(self):
		return "Choose search engine"

#Initialises LightSearch
def plugin_loaded():
	global LightSearch
	LightSearch = LightSearch()