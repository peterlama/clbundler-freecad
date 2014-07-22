from clbundler.formula import *
        
class freetype(Formula):
    version = "2.5.2"
    source = {
        "type":"archive", 
        "url":"http://sourceforge.net/projects/freetype/files/freetype2/2.5.2/ft252.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(freetype, self).__init__(context, options)
        
        self.patches.append("dll_export")
        
    def build(self):
        cmake(self.context, {"BUILD_SHARED_LIBS":"ON", "CMAKE_DEBUG_POSTFIX":"d"})
        
        vcbuild(self.context, "cmake_build\\freetype.sln", "Debug")
        vcbuild(self.context, "cmake_build\\freetype.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/freetype2"], "include", category="dev")
        files.add(["lib/*"], "lib", category="dev")
        files.add(["bin/freetype.dll"], "bin", category="rel")
        files.add(["bin/freetyped.dll"], "bin", category="dbg")
        
        return files
