from clbundler.formula import *
        
class oce(Formula):
    version = "0.15"
    source = {
        "type":"archive", 
        "url":"https://github.com/tpaviot/oce/archive/OCE-{0}.zip".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(oce, self).__init__(context, options)
        
        self.add_deps(["freeimage", "freetype", "tk"])
		
        if(context.os_name == "win"):
		    self.patches.extend(["command_limit_fix", "remove_auto_link_tcl"])
        
    def build(self):
        ft_include_dir = os.path.join(self.context.bundle_path, "include", "freetype2")
        tcl_include_dir = os.path.join(self.context.bundle_path, "include")
        tcl_lib = os.path.join(self.context.bundle_path, "lib", "tcl86t.lib")
        tcl_tclsh = os.path.join(self.context.bundle_path, "bin", "tclsh86t.exe")
        tk_lib = os.path.join(self.context.bundle_path, "lib", "tk86t.lib")
        tk_wish = os.path.join(self.context.bundle_path, "bin", "tkwish86t.exe")
        
        cmake(self.context, {"OCE_INSTALL_PREFIX":self.context.install_dir,
                             "OCE_INSTALL_BIN_DIR":"bin",
                             "OCE_INSTALL_LIB_DIR":"lib",
                             "OCE_INSTALL_CMAKE_DATA_DIR":"lib/cmake",
                             "OCE_DRAW":"ON",
                             "OCE_WITH_FREEIMAGE":"ON",
                             "OCE_USE_MSVC_EXPRESS":"ON",
							 "OCE_COPY_HEADERS_BUILD":"ON",
                             "CMAKE_CXX_FLAGS":"/DWIN32 /D_WINDOWS /W3 /GR /EHa /Zm2000",
                             "FREETYPE_INCLUDE_DIRS":ft_include_dir,
                             "TCL_INCLUDE_PATH":tcl_include_dir,
                             "TCL_LIBRARY":tcl_lib,
                             "TCL_TCLSH":tcl_tclsh,
                             "TK_INCLUDE_PATH":tcl_include_dir,
                             "TK_LIBRARY":tk_lib,
                             "TK_WISH":tk_wish})
        
        vcbuild(self.context, "cmake_build\\OCE.sln", "Debug")
        vcbuild(self.context, "cmake_build\\OCE.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*.lib", "lib/*.pdb"], "lib", category="dev")
        files.add(["lib/cmake/*"], "lib/cmake", category="dev")
        files.add(["bin/*[!d].dll"], "bin", category="rel")
        files.add(["bin/*d.dll"], "bin", category="dbg")
        
        return files
