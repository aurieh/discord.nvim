# Discord.NVIM
Discord Rich Presence for NeoVim.

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
Plug 'aurieh/discord.nvim'
```
[dein](https://github.com/Shougo/dein.vim):
```
call dein#add('aurieh/discord.nvim')
```
To finish things off, call `:UpdateRemotePlugins` and restart NeoVim.

# TODO
- [ ] Rewrite the client in pure python, no cffi
- [ ] Upload some language icons
- [ ] Make the client ID configurable
- [ ] Documentation
