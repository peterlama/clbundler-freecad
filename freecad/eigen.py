from clbundler.formula import *
        
class eigen(Formula):
    version = "3.2.1"
    source = {
        "type":"archive", 
        "url":"http://bitbucket.org/eigen/eigen/get/{0}.zip".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"], "gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(eigen, self).__init__(context, options)
       
    def build(self):
        cmake(self.context)
        
        if self.context.toolchain.startswith("vc"):
            vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
            vcbuild(self.context, vcproj, "Release")
        else:
            os.chdir("cmake_build")
            system.run_cmd("make", ["install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        
        return files
