# Discord.NVIM
Discord Rich Presence for Neovim.

# Install
Clone and build [discordapp/discord-rpc](https://github.com/discordapp/discord-rpc):
```
git clone https://github.com/discordapp/discord-rpc.git && cd discord-rpc
cmake -DBUILD_SHARED_LIBS=on .
make
```
Copy the resulting shared library to either `~/.local/lib`, `/lib` or `/usr/lib`.
```
cp src/libdiscord-rpc.so ~/.local/lib/
```
Install the plugin using your favorite plugin manager:

[Vundle](https://github.com/VundleVim/Vundle.vim):
```
Plugin 'aurieh/discord.nvim'
```
[Plug](https://github.com/junegunn/vim-plug):
```
Plug 'aurieh/discord.nvim', { 'do': ':UpdateRemotePlugins'}
```
[dein](https://github.com/Shougo/dein.vim):
```
call dein#add('aurieh/discord.nvim')
```
To finish things off, call `:UpdateRemotePlugins` and restart NeoVim.

# TODO
- [ ] Multiple clients: wait for lock
- [ ] Rewrite the client in pure python, no cffi
- [X] Upload some language icons
- [X] Make the client ID configurable
- [ ] Documentation
- [ ] Tests
- [ ] Pack ratelimit data in pidfiles
