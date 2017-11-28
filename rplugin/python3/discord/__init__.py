from .discord_rpc_native import Discord
from .pidlock import PidLock, get_tempdir
from os.path import join, basename
from time import time
import atexit
import neovim


FT_BLACKLIST = ["help"]


@neovim.plugin
class DiscordPlugin(object):
    def __init__(self, vim):
        self.vim = vim
        self.discord = None
        self.log_ = ""
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

    # @neovim.comand("DiscordStartTimer")
    # def start_timer(self):
    #     self.vim.eval(
    #         "timer_start(20, 'DiscordUpdatePresence', { 'repeat': -1 })"
    #     )
    #
    @neovim.command("DiscordUpdatePresence")
    def update_presence(self):
        if not self.lock:
            self.lock = PidLock(join(get_tempdir(), "dnvim_lock"))
        if self.locked:
            return
        if not self.discord:
            self.log("info: init")
            self.locked = not self.lock.lock()
            if self.locked:
                self.log("warn: pidfile exists")
                return
            self.discord = Discord(bytes(
                self.vim.eval("discord#GetClientID()"),
                "us-ascii"
            ))
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
                self.vim.eval("timer_stop({})".format(self.cbtimer))
            self.cbtimer = self.vim.eval(
                "timer_start(15, '_DiscordRunScheduled')"
            )
            return
        self.log("info: update presence")
        self.discord.update_presence(filename, ft, workspace)

    def get_current_buf_var(self, var):
        return self.vim.eval(
            "getbufvar({}, '{}')".format(self.vim.current.buffer.number, var)
        )

    def get_workspace(self):
        bufnr = self.vim.current.buffer.number
        dirpath = self.vim.eval("discord#GetProjectDir({})".format(bufnr))
        if dirpath:
            return basename(dirpath)
        return None

    @neovim.function("_DiscordRunScheduled")
    def run_scheduled(self, args):
        self.cbtimer = None
        self.update_presence()

    @neovim.function("DiscordGetLog", sync=True)
    def get_log(self, args):
        return self.log_

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

    def log(self, message):
        self.log_ += str(message) + "\n"

    def shutdown(self):
        self.lock.unlock()
        self.discord.shutdown()
