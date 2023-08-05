# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB

class CmdU(PyApiB):
    """
    命令行相关工具
    """

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def run(self, cmdline, cwd=None):
        import subprocess
        subprocess.Popen(cmdline, shell=True, cwd=cwd).wait()

