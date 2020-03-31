import importlib
import os


def register_blueprint():
    router = []
    dir_path = os.path.split(__file__)[0]
    for file in os.listdir(dir_path):
        module_name, ext = os.path.splitext(file)
        if not (module_name.endswith('_urls') and not ext):
            continue
        url_path = os.path.join(dir_path, module_name)
        urls_file = os.listdir(url_path)
        for url_file in urls_file:
            file_name, file_ext = os.path.splitext(url_file)
            if not (file_name.endswith('_urls') and file_ext == '.py'):
                continue
            module = importlib.import_module('.{}.{}'.format(module_name, file_name), __package__)
            router.extend(module.url_patterns)
    return router


routers = register_blueprint()
