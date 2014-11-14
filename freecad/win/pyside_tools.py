from clbundler.formula import *
        
class pyside_tools(Formula):
    version = "0.2.15"
    source = {
        "type":"archive", 
        "url":"https://github.com/PySide/Tools/archive/{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pyside_tools, self).__init__(context, options)
        
        self.add_deps("pyside")
        
    def build(self):
        py_site_packages = os.path.join(self.context.install_dir, "bin")
        cmake(self.context, {"SITE_PACKAGE":py_site_packages})
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\pyside-tools.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\pyside-tools.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["bin/*"], "bin")
        
        return files
