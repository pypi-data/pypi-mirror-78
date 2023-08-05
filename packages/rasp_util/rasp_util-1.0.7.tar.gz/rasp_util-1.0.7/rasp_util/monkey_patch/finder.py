from importlib.machinery import PathFinder, ModuleSpec


class Finder(PathFinder):

    def __init__(self, module_name, custom_loader_class):
        self.module_name = module_name
        self.custom_loader_class = custom_loader_class

    def find_spec(self, fullname, path=None, target=None):
        if fullname == self.module_name:
            spec = super().find_spec(fullname, path, target)
            loader = self.custom_loader_class(fullname, spec.origin)
            return ModuleSpec(fullname, loader)
