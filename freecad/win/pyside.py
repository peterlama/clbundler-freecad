from clbundler.formula import *
        
class pyside(Formula):
    version = "1.2.2"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases/pyside"
              "/pyside-qt4.8+{0}.tar.bz2".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pyside, self).__init__(context, options)
        
        self.add_deps(["python", "qt", "shiboken"])
        self.patches = ["clbundler_changes", "relative_install"]
        
    def build(self):
        py_site_packages = os.path.join(self.context.install_dir, "bin")
        cmake(self.context, {"SITE_PACKAGE":py_site_packages,
                             "BUILD_TESTS":"OFF"})
        
        vcbuild(self.context, "cmake_build\\pysidebindings.sln", "Debug")
        vcbuild(self.context, "cmake_build\\pysidebindings.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/cmake/*"], "lib/cmake", category="dev")
        files.add(["lib/*.lib"], "lib", category="dev")
        files.add(["bin/*[!d].dll"], "bin", category="rel")
        files.add(["bin/*_d.dll"], "bin", category="dbg")
        files.add(["bin/PySide/*[!d].pyd", "bin/PySide/*.py"], "bin/PySide", category="rel")
        files.add(["bin/PySide/*_d.pyd"], "bin/PySide", category="dbg")
        
        return files
