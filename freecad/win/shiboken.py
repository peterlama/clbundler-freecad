from clbundler.formula import *
        
class shiboken(Formula):
    version = "1.2.2"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases/pyside"
              "/shiboken-{0}.tar.bz2".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(shiboken, self).__init__(context, options)
        
        self.add_deps(["python", "qt"])
        
        self.patches = ["suffix", "relative_install"]
        if context.toolchain == "vc12":
            self.patches.append("vc12")
        
    def build(self):
        py_site_packages = os.path.join(self.context.install_dir, "bin")
        cmake(self.context, {"PYTHON_SITE_PACKAGES":py_site_packages,
                             "BUILD_TESTS":"OFF",
                             "CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE":".",
                             "CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG":"."})
        
        vcbuild(self.context, "cmake_build\\shiboken.sln", "Debug")
        vcbuild(self.context, "cmake_build\\shiboken.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/cmake/*"], "lib/cmake", category="dev")
        files.add(["lib/*.lib"], "lib", category="dev")
        files.add(["bin/shiboken.exe",
                   "bin/shiboken.pyd",
                   "bin/shiboken-python2.7.dll"], "bin", category="rel")
        files.add(["bin/shiboken_d.pyd",
                   "bin/shiboken-python2.7_d.dll"], "bin", category="dbg")
        
        return files