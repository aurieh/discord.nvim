import neovim
from .discord_rpc_native import Discord
from time import time
import atexit


@neovim.plugin
class DiscordPlugin(object):
    def __init__(self, vim):
        self.vim = vim
        self.discord = None
        # Ratelimits
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
        if not self.discord:
            self.discord = Discord(bytes(
                self.vim.eval("discord#get_clientid()"),
                "us-ascii"
            ))
            atexit.register(self.discord.shutdown)
        filename = self.vim.current.buffer.name
        ft = self.vim.eval(
            "getbufvar({}, '&ft')".format(self.vim.current.buffer.number)
        )
        if self.is_ratelimited(filename):
            if self.cbtimer:
                self.vim.eval("timer_stop({})".format(self.cbtimer))
            self.cbtimer = self.vim.eval(
                "timer_start(15, '_DiscordRunScheduled')"
            )
            return
        self.discord.update_presence(filename, ft)

    @neovim.function("_DiscordRunScheduled")
    def run_scheduled(self, args):
        self.cbtimer = None
        self.update_presence()

    def is_ratelimited(self, filename):
        if self.lastfilename == filename:
            return True
        now = time()
        if (now - self.lasttimestamp) >= 15:
            self.lastused = False
            self.lasttimestamp = now
        if self.lastused:
            return True
        self.lastused = True
