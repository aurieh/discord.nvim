# Discord.NVIM
Discord Rich Presence for Neovim.

# Platform Support
Windows is not supported. Please do not create issues if you're trying to use
this plugin in WSL: while WSL2 is supported, it is up to you to figure out how
to translate the Windows client socket to a Unix domain socket inside WSL.

# Install
```sh
$ python3 -m pip install --user --upgrade pynvim
$ DNVIM_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/discord.nvim/start/discord.nvim"
$ mkdir -p "$DNVIM_HOME"
$ git clone https://github.com/aurieh/discord.nvim.git "$DNVIM_HOME"
```
Then, in Neovim, call `:UpdateRemotePlugins`. For your custom status to show up
on Discord,
"Display currently running game as a status message" must be enabled under
**Settings** -> (App settings) **Games**.

## Uninstall
```sh
$ rm -rf "${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/discord.nvim"
```
Once again, call `:UpdateRemotePlugins`.
