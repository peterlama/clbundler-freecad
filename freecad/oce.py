from clbundler.formula import *
        
class oce(Formula):
    version = "0.16"
    source = {
        "type":"archive", 
        "url":"https://github.com/tpaviot/oce/archive/OCE-{0}.zip".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"], "gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(oce, self).__init__(context, options)
        
        self.add_deps("freeimage", "freetype", "tk")
        
    def build(self):
        ft_include_dir = os.path.join(self.context.bundle_path, "include", "freetype2")
        
        cmake_options = {"OCE_INSTALL_PREFIX":self.context.install_dir,
                         "OCE_INSTALL_BIN_DIR":"bin",
                         "OCE_INSTALL_LIB_DIR":"lib",
                         "OCE_INSTALL_CMAKE_DATA_DIR":"lib/cmake",
                         "OCE_DRAW":"ON",
                         "OCE_WITH_FREEIMAGE":"ON",
                         "OCE_USE_PCH":"ON",
                         "FREETYPE_INCLUDE_DIRS":ft_include_dir}
        
        if self.context.toolchain.startswith("vc"):
            cmake_options["OCE_USE_MSVC_EXPRESS"] = "ON"
            cmake_options["OCE_COPY_HEADERS_BUILD"] = "ON"
            cmake_options["OCE_TESTING"] = "OFF"
            cmake_options["CMAKE_CXX_FLAGS"] = "/DWIN32 /D_WINDOWS /W3 /GR /EHa /Zm2000"

        cmake(self.context, cmake_options)
        
        if self.context.toolchain.startswith("vc"):
            if "debug" in self.variant:
                vcbuild(self.context, "cmake_build\\OCE.sln", "Debug")
            if "release" in self.variant:
                vcbuild(self.context, "cmake_build\\OCE.sln", "Release")
            
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
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/cmake/*"], "lib/cmake", category=Categories.build)
        files.add(["bin/DRAWEXE*"], "bin", category=Categories.run)
        files.add(["share/oce*"], "share", category=Categories.run)

        if self.context.toolchain.startswith("vc"):
            files.add(["lib/*.lib", "lib/*.pdb"], "lib", category=Categories.build)       
            files.add(["bin/*[!d].dll"], "bin", category=Categories.run)
            files.add(["bin/*d.dll"], "bin", category=Categories.run_dbg)
        else:
            files.add(["lib/*"], "lib", exclude=["lib/cmake"], category=Categories.run)
        
        return files

