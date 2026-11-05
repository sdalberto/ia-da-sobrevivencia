"""Inicia os motores locais (llama.cpp e kiwix-serve) que estiverem no kit."""

import glob
import os
import shutil
import socket
import subprocess
import sys

from .config import LOG_DIR, MODELS_DIR, RUNTIME_DIR, ZIM_DIR, exe, is_windows, load_json, platform_key, CONFIG_DIR


def port_in_use(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def _find_in(base, names):
    if not os.path.isdir(base):
        return None
    for dirpath, _, files in os.walk(base):
        for n in names:
            if n in files:
                return os.path.join(dirpath, n)
    return None


def find_llama_server():
    plat = platform_key()
    names = [exe("llama-server")]
    found = _find_in(os.path.join(RUNTIME_DIR, "llama.cpp", plat), names)
    if found:
        return found, "llama.cpp"
    # llamafile (um único executável para todos os sistemas)
    for pattern in ("llamafile*", "llamafile*.exe"):
        for p in sorted(glob.glob(os.path.join(RUNTIME_DIR, pattern))):
            if os.path.isfile(p) and not p.endswith((".gguf", ".zip", ".part")):
                return p, "llamafile"
    which = shutil.which("llama-server")
    if which:
        return which, "llama.cpp"
    return None, None


def find_kiwix_serve():
    plat = platform_key()
    found = _find_in(os.path.join(RUNTIME_DIR, "kiwix-tools", plat), [exe("kiwix-serve")])
    if found:
        return found
    return shutil.which("kiwix-serve")


def find_model(settings):
    files = sorted(glob.glob(os.path.join(MODELS_DIR, "*.gguf")))
    if not files:
        return None
    wanted = settings.get("model_file")
    if wanted:
        for f in files:
            if os.path.basename(f) == wanted:
                return f
    cfg = load_json(os.path.join(CONFIG_DIR, "models.json"), {}) or {}
    default_id = cfg.get("default")
    for m in cfg.get("models", []):
        if m.get("id") == default_id:
            for f in files:
                if os.path.basename(f) == m.get("file"):
                    return f
    # Senão, o maior modelo presente (tende a ser o melhor que a pessoa escolheu baixar).
    return max(files, key=os.path.getsize)


def find_zims():
    return sorted(glob.glob(os.path.join(ZIM_DIR, "**", "*.zim"), recursive=True))


def _ensure_exec(path):
    if not is_windows():
        try:
            os.chmod(path, os.stat(path).st_mode | 0o111)
        except OSError:
            pass


def _env_for(binary):
    env = os.environ.copy()
    bindir = os.path.dirname(binary)
    if sys.platform == "darwin":
        env["DYLD_LIBRARY_PATH"] = bindir + os.pathsep + env.get("DYLD_LIBRARY_PATH", "")
    elif not is_windows():
        env["LD_LIBRARY_PATH"] = bindir + os.pathsep + env.get("LD_LIBRARY_PATH", "")
    # Serviços locais não devem usar proxy.
    env["NO_PROXY"] = "127.0.0.1,localhost"
    return env


def _spawn(cmd, logname):
    os.makedirs(LOG_DIR, exist_ok=True)
    log = open(os.path.join(LOG_DIR, logname), "ab")
    kwargs = {"stdout": log, "stderr": subprocess.STDOUT, "stdin": subprocess.DEVNULL, "env": _env_for(cmd[0])}
    if is_windows():
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return subprocess.Popen(cmd, **kwargs)


class Launcher:
    def __init__(self, settings, say=print):
        self.settings = settings
        self.say = say
        self.procs = []

    def start_llm(self):
        port = int(self.settings.get("llm_port", 8091))
        if port_in_use(port):
            self.say(f"  • Motor de IA já está rodando na porta {port}.")
            return True
        binary, kind = find_llama_server()
        model = find_model(self.settings)
        if not binary or not model:
            if not binary:
                self.say("  • Motor de IA (llama.cpp) não encontrado em runtime/ — rode o 'preparar-kit'.")
            if not model:
                self.say("  • Nenhum modelo .gguf em models/ — rode o 'preparar-kit'.")
            self.say("    (Se você usa Ollama, ele será detectado automaticamente.)")
            return False
        _ensure_exec(binary)
        ctx = str(self.settings.get("llm_context", 8192))
        if kind == "llamafile":
            cmd = [binary, "--server", "--nobrowser", "-m", model, "--host", "127.0.0.1", "--port", str(port), "-c", ctx]
            if is_windows() and not binary.lower().endswith(".exe"):
                self.say("  • No Windows o llamafile precisa terminar em .exe — renomeie o arquivo.")
                return False
        else:
            cmd = [binary, "-m", model, "--host", "127.0.0.1", "--port", str(port), "-c", ctx]
        threads = int(self.settings.get("llm_threads", 0) or 0)
        if threads > 0:
            cmd += ["-t", str(threads)]
        try:
            self.procs.append(_spawn(cmd, "llm.log"))
            self.say(f"  • Iniciando motor de IA: {os.path.basename(model)} (pode levar até 1 minuto para carregar)")
            return True
        except OSError as e:
            self.say(f"  • Falha ao iniciar o motor de IA: {e} (veja logs/llm.log)")
            return False

    def start_kiwix(self):
        if not self.settings.get("kiwix_enabled", True):
            return False
        port = int(self.settings.get("kiwix_port", 8092))
        if port_in_use(port):
            self.say(f"  • Kiwix já está rodando na porta {port}.")
            return True
        zims = find_zims()
        if not zims:
            self.say("  • Nenhuma base .zim em zim/ — a IA usará apenas os guias do kit.")
            return False
        binary = find_kiwix_serve()
        if not binary:
            self.say("  • kiwix-serve não encontrado. Rode o 'preparar-kit' ou ative o 'Servidor local' no Kiwix Desktop")
            self.say(f"    e ajuste kiwix_url em config/settings.local.json (atual: {self.settings.get('kiwix_url')}).")
            return False
        _ensure_exec(binary)
        cmd = [binary, "--address", "127.0.0.1", "--port", str(port)] + zims
        try:
            self.procs.append(_spawn(cmd, "kiwix.log"))
            self.say(f"  • Iniciando biblioteca Kiwix com {len(zims)} base(s).")
            return True
        except OSError as e:
            self.say(f"  • Falha ao iniciar o kiwix-serve: {e} (veja logs/kiwix.log)")
            return False

    def stop(self):
        for p in self.procs:
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        self.procs = []
