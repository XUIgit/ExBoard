from .Plugin import Plugin

class ExInterFace:

    __main_window = None

    __plugins = []

    __exclusive_plugin = None

    #一些全局设置
    __background_color = 'ffffff'

    @staticmethod
    def register(plugin):
        if isinstance(plugin, Plugin):
            #检查是否注册了同名插件
            for _plugin in ExInterFace.__plugins:
                if _plugin.getPluginName() == plugin.getPluginName():
                    raise RuntimeError("插件已经注册，请将重复的插件移出插件目录")
            ExInterFace.__plugins.append(plugin)
        else:
            raise TypeError("plugin object must inherit plugin.Plugin")

    @staticmethod
    def getPlugins():  # 获取注册了的插件
        return ExInterFace.__plugins

    @staticmethod
    def getPlugin(name):
        for plugin in ExInterFace.__plugins:
            if plugin.getPluginName() == name:
                return plugin
        raise RuntimeError("not found plugin named "+name)

    @staticmethod
    def init(mainWnd):
        ExInterFace.__main_window = mainWnd
        # 在这里完成插件的加载
        import plugins  # 执行一下插件包里的__init__的register代码 注册到Exinterface中
        #将插件注册到mainWindow中
        ExInterFace.__main_window.registerPulgins(ExInterFace.__plugins)

        print("所有插件加载完成")

    @staticmethod
    def addBorad(name):
        from .Board import Board
        board = Board(name, ExInterFace.__main_window)
        ExInterFace.applySettingToOne(board)
        return ExInterFace.__main_window.addBoard(board)

    @staticmethod
    def applySettingToOne(board):#应用全局设置到新的board
        board.setBackgroundColor(ExInterFace.__background_color)

    @staticmethod
    def applySettingToAll():
        for board in ExInterFace.__main_window.getAllBoards():
            ExInterFace.applySettingToOne(board)

    @staticmethod
    def removeBoard(b):
        ExInterFace.__main_window.removeBoard(b)

    @staticmethod
    def setBackgroundColor(color):
        ExInterFace.__background_color = color
        ExInterFace.applySettingToAll()

    @staticmethod
    def getCurrentBoard():
        return ExInterFace.__main_window.getCurrentBoard()

    @staticmethod
    def getBoard(index):
        return ExInterFace.__main_window.getBoard(index)

    @staticmethod
    def exclusive(plugin):
        '''插件独占除 paintEvent和keyEvent以外的事件'''
        for _plugin in ExInterFace.__plugins:
            if _plugin is plugin:
                ExInterFace.__exclusive_plugin = plugin
            else:
                _plugin.otherExlusive()

    @staticmethod
    def getExclusivePlugin():
        return ExInterFace.__exclusive_plugin