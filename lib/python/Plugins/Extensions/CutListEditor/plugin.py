from Plugins.Plugin import PluginDescriptor


def CutListEditor(session, service=None):
	from Plugins.Extensions.CutListEditor import ui
	return ui.CutListEditor(session, service)


def main(session, service, **kwargs):
	session.open(CutListEditor, service)


def Plugins(**kwargs):
	return PluginDescriptor(name=_("Cutlist editor"), description=_("Cutlist editor..."),
		where=PluginDescriptor.WHERE_MOVIELIST, needsRestart=False, fnc=main)
