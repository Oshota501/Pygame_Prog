from setuptools import setup, Extension
import pybind11

# pybind11.get_include() でヘッダーファイルの場所を教えてあげる
ext_modules = [
    Extension(
        "vector",        # モジュール名
        ["vector.cpp"],  # ソースファイル
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name="vector",
    version="0.1",
    ext_modules=ext_modules,
)