from clbundler.formula import *
        
class setuptools(Formula):
    version = "5.4.1"
    source = {
        "type":"archive",
        "url":"https://pypi.python.org/packages/source/s/setuptools/setuptools-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(setuptools, self).__init__(context, options)
        
        self.add_deps("python")
        
    def build(self):
        distutils(self.context)
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["Lib/site-packages/*"], "bin/Lib/site-packages")
        files.add(["Scripts/easy_install.exe", "Scripts/easy_install-script.py"], "bin")
        
        return files
        