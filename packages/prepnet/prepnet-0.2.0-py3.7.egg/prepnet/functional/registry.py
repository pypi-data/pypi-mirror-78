from prepnet.functional.configuration_context import ConfigurationContext

def register_converter(name):
    def _(klass):
        return klass
    return _
ConfigurationContext.aaa = lambda x, y: x + y
