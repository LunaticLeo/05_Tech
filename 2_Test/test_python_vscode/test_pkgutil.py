import pkgutil

# import sys

import test_modules

name = [info.name for info in pkgutil.iter_modules(test_modules.__path__)]
print(name)

pathentry = [pathentry for pathentry in test_modules.__path__]

importer = pkgutil.get_importer(pathentry[0])      # 拿到 PyInstaller 的导入器
archive = getattr(importer, "_pyz_archive", None) # 拿到 PYZ 归档对象
toc = getattr(archive, "toc", None)              # toc = 模块名表

print(importer)
print(archive)
print(toc)