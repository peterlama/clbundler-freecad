from clbundler.formula import *
        
class zlib(Formula):
    version = "1.2.8"
    source = {
        "type":"archive", 
        "url":"http://zlib.net/zlib-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(zlib, self).__init__(context, options)
       
    def build(self):
        cmake(self.context)
        
        vcbuild(self.context, "cmake_build\\zlib.sln", "Debug")
        vcbuild(self.context, "cmake_build\\zlib.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*"], "lib", category="dev")
        files.add(["bin/zlib.dll"], "bin", category="rel")
        files.add(["bin/zlibd.dll"], "bin", category="dbg")
        
        return files
