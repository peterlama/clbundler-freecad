from clbundler.formula import *
        
class python(Formula):
    version = "2.7.8"
    source = {
        "type":"archive", 
        "url":"https://www.python.org/ftp/python/{0}/Python-{0}.tgz".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(python, self).__init__(context, options)
        
        self.add_deps(["tk"])
        
    def build(self):
        configure(self.context, ["--with-tcltk-includes='-I" + self.context.bundle_path + "/include'", 
                                 "--with-tcltk-libs='" + self.context.bundle_path + "/lib'",
                                 "--enable-shared"])
        
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*.dylib"], "lib", category="rel")
        files.add(["lib/python2.7"], "lib", category="rel")
        files.add(["bin/*"], "bin", category="rel")
        
        return files
