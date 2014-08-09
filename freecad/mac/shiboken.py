from clbundler.formula import *
        
class shiboken(Formula):
    version = "1.2.2"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases/pyside"
              "/shiboken-{0}.tar.bz2".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(shiboken, self).__init__(context, options)
        
        self.add_deps(["python", "qt"])
        
        self.patches = ["relative_install"]
        
    def build(self):
        py_site_packages = self.context.install_dir + "/lib/python2.7/site-packages"
        cmake(self.context, {"PYTHON_SITE_PACKAGES":py_site_packages,
                             "BUILD_TESTS":"OFF"})
        
        os.chdir("cmake_build")
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install/fast"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/cmake/*"], "lib/cmake", category="dev")
        files.add(["lib/*.dylib"], "lib", category="dev")
        files.add(["lib/python2.7/site-packages/*"], "lib/pytyhon2.7/site-packages")
        files.add(["bin/*"], "bin", category="rel")
        
        return files
