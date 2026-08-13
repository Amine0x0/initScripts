import logging
import webbrowser
import subprocess
import shutil
from pathlib import Path

RESET = "\033[0m"
GREEN = "\033[92m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

enable_tab_launch = False

class TabLauncher:
    def __init__(self, url):
        logger.info("Running TabLauncher from [%s]", __file__)
        self._url = url

    def openlink(self):
        try:
            subprocess.Popen(
                ["google-chrome", self._url],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True
            )
            logger.info(f"{GREEN}Launched detached Chrome instance silently.{RESET}")
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
            
            subprocess.run(
                ["/bin/bash", str(filepath)],
                capture_output=False,
                text=True,
                check=True
            )
            logger.info(f"{GREEN}Script executed successfully: {script}{RESET}")

    def clean(self):
        cclean_path = shutil.which("cclean")
        if cclean_path:
            subprocess.run(
                [cclean_path],
                capture_output=False,
                text=False,
                check=False,
            )
            logger.info(f"{GREEN}cleaned some space *wink*{RESET}")
            
            usage = shutil.disk_usage(Path.home())
            logger.info(f"{CYAN}Free disk space: {usage.free / (1024**3):.2f} GB{RESET}")
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
            logger.info(f"{GREEN}Cleaner_42 executed and cleaned successfully!{RESET}")

    def keyboard_layout(self):
        layout = "us"
        subprocess.run(
            ["setxkbmap", layout],
            capture_output=False,
            text=True,
            check=True
        )
        logger.info(f"{GREEN}Keyboard layout set to {layout}{RESET}")
        
    def set_resolution(self, width=2560, height=1440, rate=60.0):
        try:
            output_res = subprocess.run(
                ["xrandr"], capture_output=True, text=True, check=True
            )
            
            active_output = None
            for line in output_res.stdout.splitlines():
                if " connected" in line:
                    active_output = line.split()[0]
                    break
            
            if not active_output:
                logger.warning("No active display output found via xrandr.")
                return

            logger.info("Setting resolution for display [%s] to %dx%d @ %sHz", active_output, width, height, rate)
            
            subprocess.run(
                ["xrandr", "--output", active_output, "--mode", f"{width}x{height}", "--rate", str(rate)],
                capture_output=False,
                text=True,
                check=True
            )
            logger.info(f"{GREEN}Resolution applied successfully ({width}x{height} @ {rate}Hz)!{RESET}")
            
        except subprocess.CalledProcessError as e:
            logger.error("Failed to set resolution: %s", e)
        except FileNotFoundError:
            logger.warning("xrandr utility not found.")

    def update_repositories(self, workspace_path=None):
            if workspace_path is None:
                workspace_path = Path.home() / "workspace"

            if not workspace_path.exists():
                logger.warning(f"{YELLOW}Workspace path not found: {workspace_path}{RESET}")
                return

            logger.info(f"{CYAN}Scanning workspace for Git repositories in: {workspace_path}{RESET}")
            
            git_dirs = [git_path.parent for git_path in workspace_path.rglob(".git")]

            if not git_dirs:
                logger.warning(f"{YELLOW}No Git repositories found in {workspace_path}{RESET}")
                return

            logger.info(f"{PURPLE}found repositories:{RESET}")
            for repo in git_dirs:
                logger.info(f"{PURPLE}  - {repo.name} ({repo}){RESET}")

            for repo in git_dirs:
                try:
                    status_res = subprocess.run(
                        ["git", "-C", str(repo), "status", "--porcelain"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    if status_res.stdout.strip():
                        logger.warning(f"{YELLOW}Skipping [{repo.name}]: Uncommitted changes detected.{RESET}")
                        continue

                    logger.info(f"Pulling latest changes for: {repo.name}...")
                    subprocess.run(
                        ["git", "-C", str(repo), "pull", "--ff-only"],
                        capture_output=False,
                        text=True,
                        check=True
                    )
                    logger.info(f"{GREEN}Successfully updated: {repo.name}{RESET}")

                except subprocess.CalledProcessError as e:
                    err_msg = e.stderr.strip() if getattr(e, 'stderr', None) else str(e)
                    logger.error(f"{RED}Failed to update repository [{repo.name}]: {err_msg}{RESET}")

if __name__ == "__main__":
    scripts = ["installgo.sh", "installcode.sh"]
    setup = SetupDesktop(scripts)
    setup.execute()
    setup.clean()
    setup.keyboard_layout()
    setup.set_resolution()
    setup.update_repositories()
    if enable_tab_launch:
        p = TabLauncher("https://profile.intra.42.fr/")
        p.openlink()