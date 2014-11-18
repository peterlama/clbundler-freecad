from clbundler.formula import *
        
class pyside(Formula):
    version = "1.2.2"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases/pyside"
              "/pyside-qt4.8+{0}.tar.bz2".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pyside, self).__init__(context, options)
        
        self.add_deps("python", "qt", "shiboken")
        self.patches = ["clbundler_changes", "relative_install"]
        
    def build(self):
        py_site_packages = os.path.join(self.context.install_dir, "bin")
        cmake(self.context, {"SITE_PACKAGE":py_site_packages,
                             "BUILD_TESTS":"OFF"})
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\pysidebindings.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\pysidebindings.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        files = FileSet()
        files.add(["cmake_build/libpyside/Debug/*.pdb"], "bin", category=Categories.run_dbg)
        
        os.chdir(self.context.install_dir)
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/cmake/*"], "lib/cmake", category=Categories.build)
        files.add(["lib/*.lib"], "lib", category=Categories.build)
        files.add(["share/PySide"], "share", category=Categories.build)
        files.add(["bin/*[!d].dll"], "bin", category=Categories.run)
        files.add(["bin/*_d.dll"], "bin", category=Categories.run_dbg)
        files.add(["bin/PySide/*[!d].pyd", "bin/PySide/*.py"], "bin/PySide", category=Categories.run)
        files.add(["bin/PySide/*_d.pyd"], "bin/PySide", category=Categories.run_dbg)
        
        return files
