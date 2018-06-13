# Discord.NVIM
Discord Rich Presence for Neovim.

# Install
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
To finish things off, call `:UpdateRemotePlugins` and restart Neovim.

# TODO
- [ ] Multiple clients: wait for lock
- [X] Rewrite the client in pure python, no cffi
- [X] Upload some language icons
- [X] Make the client ID configurable
- [X] Documentation
- [ ] Tests
- [ ] Pack ratelimit data in pidfiles
- [ ] Yarp
- [X] Activation on demand
