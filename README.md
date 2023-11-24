# Discord.NVIM
Discord Rich Presence for Neovim.

# Platform Support
Windows is not supported. Please do not create issues if you're trying to use
this plugin in WSL: while WSL2 is supported, it is up to you to figure out how
to translate the Windows client socket to a Unix domain socket inside WSL.

# Documentation
This plugin is fully documented using the built-in help system: see `:help
discord`. If this doesn't work, you might need to run `:helptags ALL`.

# Install
First, make sure that you have the Python remote plugin client. Install it via
your distribution's package manager: usually, the package name is either
`python3-neovim` (Void, Fedora), `python3-pynvim` (Ubuntu, Debian) or
`python-pynvim` (Arch).

If you've verified that your distribution does not package pynvim, install it
for your user with:
```sh
$ python3 -m pip install --user --upgrade pynvim
```
Do note that this will break when the system Python upgrades, so you'll need to
reinstall the package.

Then, install the plugin using your preferred plugin manager. If you don't have
one, use Neovim's built-in packages feature:
```
$ DNVIM_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/discord.nvim/start/discord.nvim"
$ mkdir -p "$DNVIM_HOME"
$ git clone https://github.com/aurieh/discord.nvim.git "$DNVIM_HOME"
```

Once you have it installed, call `:UpdateRemotePlugins` in Neovim if your
plugin manager hasn't done so already. You *will* need to do this again if you
update the plugin.

**Important:** For your custom status to show up on Discord, "Display current
activity as a status message." must be enabled under **Settings** -> (Activity
Settings) **Activity Privacy**.

## Uninstall
Use your plugin manager or, if you followed the procedure described above, do:
```sh
$ rm -rf "${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/discord.nvim"
```
Once again, call `:UpdateRemotePlugins`.
