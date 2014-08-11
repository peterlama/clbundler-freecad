from clbundler.formula import *
        
class libpng(Formula):
    version = "1.6.12"
    source = {
        "type":"archive", 
        "url":"http://sourceforge.net/projects/libpng/files/libpng16/1.6.12/lpng1612.7z"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(libpng, self).__init__(context, options)
        
        self.add_deps(["zlib"])
        
    def build(self):
        cmake(self.context, {"PNG_STATIC":"OFF"})
        
        vcbuild(self.context, "cmake_build\\libpng.sln", "Debug")
        vcbuild(self.context, "cmake_build\\libpng.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/png.h", "include/pngconf.h", "include/pnglibconf.h"], "include", category=Categories.build)
        files.add(["lib/*.lib"], "lib", category=Categories.build)
        files.add(["lib/libpng"], "lib/cmake", category=Categories.build)
        files.add(["bin/libpng16.dll"], "bin", category=Categories.run)
        files.add(["bin/libpng16d.dll"], "bin", category=Categories.run_dbg)
        
        return files
