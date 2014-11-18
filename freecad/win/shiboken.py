from clbundler.formula import *
        
class shiboken(Formula):
    version = "1.2.2"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases/pyside"
              "/shiboken-{0}.tar.bz2".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(shiboken, self).__init__(context, options)
        
        self.add_deps("python", "qt")
        
        self.patches = ["suffix", "relative_install"]
        if context.toolchain == "vc12":
            self.patches.append("vc12")
        
    def build(self):
        py_site_packages = os.path.join(self.context.install_dir, "bin")
        cmake(self.context, {"PYTHON_SITE_PACKAGES":py_site_packages,
                             "BUILD_TESTS":"OFF",
                             "CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE":".",
                             "CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG":"."})
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\shiboken.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\shiboken.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        files = FileSet()
        files.add(["cmake_build/libshiboken/*.pdb"], "bin", category=Categories.run_dbg)
        
        os.chdir(self.context.install_dir)
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/cmake/*"], "lib/cmake", category=Categories.build)
        files.add(["lib/*.lib"], "lib", category=Categories.build)
        files.add(["bin/shiboken.exe",
                   "bin/shiboken.pyd",
                   "bin/shiboken-python2.7.dll"], "bin", category=Categories.run)
        files.add(["bin/shiboken_d.pyd",
                   "bin/shiboken-python2.7_d.dll"], "bin", category=Categories.run_dbg)
        
        return files
