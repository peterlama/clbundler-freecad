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
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\zlib.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\zlib.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*"], "lib", category=Categories.build)
        files.add(["bin/zlib.dll"], "bin", category=Categories.run)
        files.add(["bin/zlibd.dll"], "bin", category=Categories.run_dbg)
        
        return files
