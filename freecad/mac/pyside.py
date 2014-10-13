from clbundler.formula import *
        
class pyside(Formula):
    version = "1.2.2"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases/pyside"
              "/pyside-qt4.8+{0}.tar.bz2".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(pyside, self).__init__(context, options)
        
        self.add_deps("python", "qt", "shiboken")
        self.patches = ["clbundler_changes", "relative_install"]
        
    def build(self):
        py_site_packages = self.context.install_dir + "/lib/python2.7/site-packages"
        cmake(self.context, {"SITE_PACKAGE":py_site_packages,
                             "BUILD_TESTS":"OFF"})
        
        os.chdir("cmake_build")
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install/fast"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["share/PySide"], "share", category=Categories.build)
        files.add(["lib/cmake/*"], "lib/cmake", category=Categories.build)
        files.add(["lib/*.dylib"], "lib", category=Categories.build)
        files.add(["lib/python2.7/site-packages/*"], "lib/pytyhon2.7/site-packages")
        files.add(["bin/*"], "bin", category=Categories.run)
        
        return files
