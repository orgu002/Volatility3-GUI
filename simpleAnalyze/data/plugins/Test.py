class Plugin:
    def __init__(self, name):
        self.name = name
    
    def analyze_data(self, data):
        pass

class PluginManager:
    def __init__(self):
        self.plugins = []
    
    def create_rectangle1(self, plugin):
        self.plugins.append(plugin)
    
    def get_plugins(self):
        return self.plugins

class UserPlugin(Plugin):
    def __init__(self, name):
        super().__init__(name)
    
    def analyze_data(self, data):
        if self.name == "første_plugin":
            pass
        elif self.name == "andre_plugin":
            pass
        elif self.name == "tredje_plugin":
            pass
        elif self.name == "fjerde_plugin":
            pass

class TestExporter:
    def export_test_initializing(self, initializing):
        
        print("Exporting test Initializing")
        for initializing in initializing:
            print(initializing)

if __name__ == "__main__":
    plugin_manager = PluginManager()
    
    plugin_manager.create_rectangle1(UserPlugin("første_plugin"))
    plugin_manager.create_rectangle1(UserPlugin("andre_plugin"))
    plugin_manager.create_rectangle1(UserPlugin("tredje_plugin"))
    plugin_manager.create_rectangle1(UserPlugin("fjerde_plugin"))
    
    plugindata = [...]  
    test_line = []
    for plugin in plugin_manager.get_plugins():
        result = plugin.analyze_data(plugindata)
        test_line.append(result)
    
    test_exporter = TestExporter()
    test_exporter.export_test_results(test_line)
