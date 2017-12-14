from .discord_rpc import Discord, NoDiscordClientError, ReconnectError
from .pidlock import PidLock, get_tempdir
from contextlib import contextmanager
from os.path import join, basename
from time import time
import atexit
import neovim


FT_BLACKLIST = ["help", "nerdtree"]


@contextmanager
def handle_lock(plugin):
    try:
        yield
    except NoDiscordClientError:
        plugin.locked = True
        plugin.log_warning("local discord client not found")
    except ReconnectError:
        plugin.locked = True
        plugin.log_error("ran out of reconnect attempts")


@neovim.plugin
class DiscordPlugin(object):
    def __init__(self, vim):
        self.vim = vim
        self.discord = None
        # Ratelimits
        self.lock = None
        self.locked = False
        self.lastfilename = None
        self.lastused = False
        self.lasttimestamp = time()
        self.cbtimer = None

    @neovim.autocmd("BufEnter", "*")
    def on_bufenter(self):
        self.update_presence()

    @neovim.command("DiscordUpdatePresence")
    def update_presence(self):
        if not self.lock:
            self.lock = PidLock(join(get_tempdir(), "dnvim_lock"))
        if self.locked:
            return
        if not self.discord:
            client_id = self.vim.vars.get("discord_clientid")
            reconnect_threshold = \
                self.vim.vars.get("discord_reconnect_threshold")
            self.locked = not self.lock.lock()
            if self.locked:
                self.log_warning("pidfile exists")
                return
            self.discord = Discord(client_id, reconnect_threshold)
            with handle_lock(self):
                try:
                    self.discord.connect()
                except:
                    self.log_debug("connection failed")
                    return
                self.log_debug("init")
            if self.locked:
                return
            atexit.register(self.shutdown)
        ro = self.get_current_buf_var("&ro")
        if ro:
            return
        filename = self.vim.current.buffer.name
        if not filename:
            return
        ft = self.get_current_buf_var("&ft")
        if ft in FT_BLACKLIST:
            return
        workspace = self.get_workspace()
        if self.is_ratelimited(filename):
            if self.cbtimer:
                self.vim.call("timer_stop", self.cbtimer)
            self.cbtimer = self.vim.call(
                "timer_start", 15, "_DiscordRunScheduled"
            )
            return
        self.log_debug("update presence")
        with handle_lock(self):
            self._update_presence(filename, ft, workspace)

    def _update_presence(self, filename, ft, workspace):
        activity = {}
        activity["details"] = "Editing {}".format(basename(filename))
        activity["assets"] = {
            "large_text": "The One True Editor",
            "large_image": "neovim"
        }
        activity["timestamps"] = {"start": time()}
        if ft:
            if len(ft) == 1:
                ft = "lang_{}".format(ft)
            activity["assets"]["small_text"] = ft
            activity["assets"]["small_image"] = ft
        if workspace:
            activity["state"] = "Working on {}".format(workspace)
        self.discord.set_activity(activity, self.vim.call("getpid"))

    def get_current_buf_var(self, var):
        return self.vim.call("getbufvar", self.vim.current.buffer.number, var)

    def get_workspace(self):
        bufnr = self.vim.current.buffer.number
        dirpath = self.vim.call("discord#GetProjectDir", bufnr)
        if dirpath:
            return basename(dirpath)
        return None

    @neovim.function("_DiscordRunScheduled")
    def run_scheduled(self, args):
        self.cbtimer = None
        self.update_presence()

    def is_ratelimited(self, filename):
        if self.lastfilename == filename:
            return True
        self.lastfilename = filename
        now = time()
        if (now - self.lasttimestamp) >= 15:
            self.lastused = False
            self.lasttimestamp = now
        if self.lastused:
            return True
        self.lastused = True

    def log_debug(self, message, trace=None):
        self.vim.call("discord#LogDebug", message, trace)

    def log_warning(self, message, trace=None):
        self.vim.call("discord#LogWarn", message, trace)

    def log_error(self, message, trace=None):
        self.vim.call("discord#LogError", message, trace)

    def shutdown(self):
        self.lock.unlock()
        self.discord.shutdown()
