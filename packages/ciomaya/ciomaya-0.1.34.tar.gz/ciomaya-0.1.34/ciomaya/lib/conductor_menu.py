import pymel.core as pm
 
import webbrowser
import webbrowser
from ciomaya.lib import window

MAYA_PARENT_WINDOW = 'MayaWindow'
CONDUCTOR_MENU = 'ConductorMenu'
CONDUCTOR_DOCS = 'https://docs.conductortech.com/'
LOG_LEVELS = ["CRITICAL","ERROR", "WARNING", "INFO", "DEBUG"]
DEFAULT_LOG_LEVEL=LOG_LEVELS[2]

class ConductorMenu(object):
    def __init__(self):
        if not pm.about(batch=True):
            pm.setParent(MAYA_PARENT_WINDOW)
            self.menu = pm.menu(CONDUCTOR_MENU, label="Conductor",
                                tearOff=True, pmc=pm.Callback(self.post_menu_command))
            self.jobs_menu = pm.menuItem(label="Submitter", subMenu=True)
            pm.setParent(self.menu, menu=True)
            pm.menuItem(divider=True)
            self.log_level_menu = self.build_log_level_menu()
            pm.setParent(self.menu, menu=True)
            pm.menuItem(divider=True)
            self.help_menu = pm.menuItem(label="Help", command=pm.Callback(webbrowser.open, CONDUCTOR_DOCS, new=2))
            self.about_menu = pm.menuItem(label="About", command=pm.Callback(window.show_about))

    def build_log_level_menu(self):
        result = pm.menuItem(label="Log level", subMenu=True)
        for  level in  LOG_LEVELS:
            pm.menuItem(label=level, radioButton=(level==DEFAULT_LOG_LEVEL),
                        command=pm.Callback(self.set_log_level, level))
        return result

    def post_menu_command(self):
        """
        Build the Select/Create submenu just before the menu is opened.
        """
        pm.setParent(self.jobs_menu,   menu=True)
        pm.menu(self.jobs_menu, edit=True, deleteAllItems=True)
        for j in pm.ls(type="conductorRender"):
            pm.menuItem(label="Select {}".format(str(j)),
                        command=pm.Callback(select_and_edit, j))
        pm.menuItem(divider=True)
        pm.menuItem(label="Create",  command=pm.Callback(create_and_edit))
        pm.setParent(self.menu, menu=True)

    def set_log_level(self, level):
        print "Setting Conductor log level to '{}'".format(level)

def create_and_edit():
    select_and_edit(pm.createNode("conductorRender"))
 
def select_and_edit(node):
    pm.select(node)
    if not pm.mel.isAttributeEditorRaised():
        pm.mel.openAEWindow()

def unload():
    if pm.menu(CONDUCTOR_MENU, q=True, exists=True):
        pm.menu(CONDUCTOR_MENU, e=True, deleteAllItems=True)
        pm.deleteUI(CONDUCTOR_MENU)

def load():
    unload()
    ConductorMenu()
