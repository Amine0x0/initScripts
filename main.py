import logging
import webbrowser
import subprocess
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TabLauncher:
    def __init__(self, url):
        logger.info("running TabLauncher from [%s]", __file__)
        self._url = url

    def openlink(self):
        try:
            subprocess.Popen(
                ["google-chrome", self._url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            logger.info("Launched detached Chrome instance.")
        except FileNotFoundError:
            logger.warning("Google Chrome binary not found, falling back to python webbrowser module.")
            webbrowser.open_new(self._url)

class SetupDesktop:
    def __init__(self, scripts):
        self._scripts = scripts

    def execute(self):
        base_dir = Path.cwd() / "scripts"
        
        for script in self._scripts:
            filepath = base_dir / script
            
            if not filepath.exists():
                logger.error("Script not found at path: %s", filepath)
                continue

            logger.info("Executing script: %s", filepath)
            
            proc = subprocess.run(
                ["/bin/bash", str(filepath)],
                capture_output=False,
                text=True,
                check=True
            )
            logger.info("scripts executed!")

    def clean(self):
        cclean_path = shutil.which("cclean")
        if cclean_path:
            subprocess.run(
                [cclean_path],
                capture_output=False,
                text=False,
                check=False,
            )
            logger.info("cleaned some space *wink*")
            
            usage = shutil.disk_usage(Path.home())
            logger.info("Free disk space: %.2f GB", usage.free / (1024**3))
        else:
            logger.info("cclean not found. Cloning Cleaner_42 locally...")
            
            repo_dir = Path.cwd() / "Cleaner_42"

            if repo_dir.exists():
                shutil.rmtree(repo_dir)

            subprocess.run(
                ["git", "clone", "https://github.com/ombhd/Cleaner_42.git", str(repo_dir)],
                capture_output=False,
                text=True,
                check=True,
            )

            installer_path = repo_dir / "CleanerInstaller.sh"
            subprocess.run(
                ["bash", str(installer_path)],
                check=True
            )
            
            if repo_dir.exists():
                logger.info("Removing temporary repo folder: %s", repo_dir)
                shutil.rmtree(repo_dir)

    def keyboard_layout(self):
            layout = "us"
            subprocess.run(
                ["setxkbmap", layout],
                capture_output=False,
                text=True,
                check=True
            )
        
        
if __name__ == "__main__":

    scripts = ["installgo.sh"]
    setup = SetupDesktop(scripts)
    setup.execute()
    setup.clean()
    setup.keyboard_layout()

    p = TabLauncher("https://profile.intra.42.fr/")
    p.openlink()
