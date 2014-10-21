from clbundler.formula import *
from clbundler.fileutils import makedirs
        
class matplotlib(Formula):
    version = "1.4.1"
    source = {
        "type":"archive",
        "url":"https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-{0}/"
              "matplotlib-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(matplotlib, self).__init__(context, options)
        
        self.patches = ["bundle_libs"]
        
        self.add_deps("setuptools", "numpy", "freetype", "libpng", "pyside")
        
    def build(self):
        self.context.env["INCLUDE"] += self.context.bundle_path + "\\include;"
        self.context.env["INCLUDE"] += self.context.bundle_path + "\\include\\python2.7;"
        self.context.env["INCLUDE"] += self.context.bundle_path + "\\include\\freetype2;"
        self.context.env["LIB"] += self.context.bundle_path + "\\lib;"
        
        tmp_site_packages = self.context.install_dir + "\\Lib\site-packages"
        makedirs(tmp_site_packages, exist_ok=True)
        self.context.env["PYTHONPATH"] = tmp_site_packages
        
        with open("setup.cfg", "w") as f:
            content = ("[packages]\n"
                       "tests = False\n"
                       "sample_data = False\n"
                       "[gui_support]\n"
                       "pyside = True\n"
                       "tkagg = False\n")
            f.write(content)
        
        system.run_cmd("easy_install", ["--install-dir=" + tmp_site_packages, "pyparsing"])
        system.run_cmd("easy_install", ["--install-dir=" + tmp_site_packages, "python-dateutil"])
        system.run_cmd("python", ["setup.py", "install", "--single-version-externally-managed", "--root=" + self.context.install_dir, "--prefix=."])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["Lib/site-packages/*"], "bin/Lib/site-packages")
        
        return files
        