from clbundler.formula import *
        
class freetype(Formula):
    version = "2.5.2"
    source = {
        "type":"archive", 
        "url":"http://sourceforge.net/projects/freetype/files/freetype2/2.5.2/ft252.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"], "gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(freetype, self).__init__(context, options)
        
        if context.os_name == "win":
            self.patches.append("dll_export")
        
    def build(self):
        cmake(self.context, {"BUILD_SHARED_LIBS":"ON", 
                             "CMAKE_DEBUG_POSTFIX":"d",
                             "CMAKE_BUILD_TYPE":"Release"})
        
        if self.context.toolchain.startswith("vc"):
            if "debug" in self.variant:
                vcbuild(self.context, "cmake_build\\freetype.sln", "Debug")
            if "release" in self.variant:
                vcbuild(self.context, "cmake_build\\freetype.sln", "Release")
            
            vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
            if "debug" in self.variant:
                vcbuild(self.context, vcproj, "Debug")
            if "release" in self.variant:
                vcbuild(self.context, vcproj, "Release")
        else:
            os.chdir("cmake_build")
            system.run_cmd("make", ["-j4"])
            system.run_cmd("make", ["install/fast"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/freetype2"], "include", category=Categories.build)

        if self.context.toolchain.startswith("vc"):
            files.add(["lib/*"], "lib", category=Categories.build)
            files.add(["bin/freetype.dll"], "bin", category=Categories.run)
            files.add(["bin/freetyped.dll"], "bin", category=Categories.run_dbg)
        else:
            if self.context.os_name == "mac":
                files.add(["lib/*.dylib"], "lib", category=Categories.run)
            else:
                files.add(["lib/*.so"], "lib", category=Categories.run)
        
        return files

