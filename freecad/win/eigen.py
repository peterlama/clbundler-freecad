from clbundler.formula import *
        
class eigen(Formula):
    version = "3.2.1"
    source = {
        "type":"archive", 
        "url":"http://bitbucket.org/eigen/eigen/get/{0}.zip".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(eigen, self).__init__(context, options)
       
    def build(self):
        cmake(self.context)
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        
        return files