"""
Checks if modules are installed.
Uninstalled modules are returned.
"""
def check_modules_installed(modules):

    import imp
    not_installed_modules = []
    for module_name in modules:
        try:
            imp.find_module(module_name)
        except ImportError as e:
            # We also test against a rare case: module is an egg file
            try:
                __import__(module_name)
            except ImportError as e:
                not_installed_modules.append(module_name)

    return not_installed_modules
