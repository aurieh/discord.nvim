import neovim
from .discord_rpc_native import Discord
from time import time
import atexit


@neovim.plugin
class DiscordPlugin(object):
    def __init__(self, vim):
        self.vim = vim
        self.discord = Discord(b"382909573021040650")
        # Ratelimits
        self.lastfilename = None
        self.numreqs = 0
        self.lasttimestamp = time()
        atexit.register(self.discord.shutdown)

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
        filename = self.vim.current.buffer.name
        ft = self.vim.eval(
            "getbufvar({}, '&ft')".format(self.vim.current.buffer.number)
        )
        if self.is_ratelimited(filename):
            return
        self.discord.update_presence(filename, ft)

    def is_ratelimited(self, filename):
        if self.lastfilename == filename:
            return True
        now = time()
        if (now - self.lasttimestamp) >= 60:
            self.lasttimestamp = now
            self.numreqs = 0
        self.numreqs += 1
        if self.numreqs > 5:
            return True
