import os
os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire
from wkmake.make import make_from_files
from wkmake.pkg_info import pkg_templates_dir,PkgData
from wkmake.utils import export
class CLI:
    def hi(cls):
        print('Hi, I am wkmake.'.center(50, '*'))
    def make(self,cfg='wkmake.json',src='python_package',dst='./wkmake-output',overwrite=False):
        if not os.path.exists(src):
            src2=os.path.join(pkg_templates_dir,src)
            if not os.path.exists(src2):
                raise FileNotFoundError('Make source %s not found.'%(src))
            else:
                src=src2
        make_from_files(src,dst,config_files=[cfg],overwrite=overwrite)
    def export(self,demo=True,dst=None):
        dst=dst or './export-output'
        if demo:
            export(PkgData.Paths.example,dst)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()