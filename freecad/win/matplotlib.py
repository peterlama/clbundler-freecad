from clbundler.formula import *
from clbundler.fileutils import makedirs
        
class matplotlib(Formula):
    version = "1.4.2"
    source = {
        "type":"archive",
        "url":"https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-{0}/"
              "matplotlib-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(matplotlib, self).__init__(context, options)
        
        self.patches = ["bundle_libs"]
        
        self.add_deps("setuptools", "numpy", "freetype", "libpng", "pyside")
        
    def build(self):
        self.context.env["INCLUDE"] += self.context.bundle_path + "\\include\\python2.7;"
        self.context.env["INCLUDE"] += self.context.bundle_path + "\\include\\freetype2;"
        
        tmp_site_packages = self.context.install_dir + "\\Lib\site-packages"
        makedirs(tmp_site_packages, exist_ok=True)
        self.context.env["PYTHONPATH"] = tmp_site_packages
        
        with open("setup.cfg", "w") as f:
            content = ("[packages]\n"
                       "tests = False\n"
                       "sample_data = False\n"
                       "[gui_support]\n"
                       "pyside = True\n"
                       "tkagg = False\n"
                       "[rc_options]\n"
                       "backend = Agg\n"
                       "[directories]\n"
                       "basedirlist = " + self.context.bundle_path)
            f.write(content)
        
        system.run_cmd("easy_install", ["--install-dir=" + tmp_site_packages, "six"])
        system.run_cmd("easy_install", ["--install-dir=" + tmp_site_packages, "pyparsing"])
        system.run_cmd("easy_install", ["--install-dir=" + tmp_site_packages, "python-dateutil"])
        
        if "debug" in self.variant:
            self.context.env["LINK"] = "freetyped.lib "
            self.context.env["LINK"] += "libpng16d.lib "
            
            system.run_cmd("python", ["setup.py", "build", "--debug"])
        if "release" in self.variant:
            self.context.env["LINK"] = "freetype.lib "
            self.context.env["LINK"] += "libpng16.lib "
            
            system.run_cmd("python", ["setup.py", "build"])
        
        system.run_cmd("python", ["setup.py", "install", "--single-version-externally-managed", "--root=" + self.context.install_dir, "--prefix=."])
        
        os.chdir(self.context.install_dir)
        
        #make paths relative
        new_pth = ""
        with open("Lib/site-packages/easy-install.pth") as f:
            for line in f:
                new_pth += line.replace(self.context.bundle_path.lower() + "\\bin\\lib\\site-packages", ".")
        with open("Lib/site-packages/easy-install.pth", "w") as f:
            f.write(new_pth)
        
        files = FileSet()
        files.add(["Lib/site-packages/*"], "bin/Lib/site-packages")
        
        return files
        