if !has('nvim')
  echoerr 'This plugin requires Neovim'
  finish
endif
if !has('timers')
  echoerr 'This plugin requires +timers build option'
  finish
endif
if !has('python3')
  echoerr 'This plugin requires python3'
  finish
endif

if !exists('g:discord_activate_on_enter')
    let g:discord_activate_on_enter = 1
endif
if !exists('g:discord_clientid')
  let g:discord_clientid = '383069395896762369'
endif
if !exists('g:discord_reconnect_threshold')
  let g:discord_reconnect_threshold = 5
endif
if !exists('g:discord_log_debug')
  let g:discord_log_debug = 0
endif
if !exists('g:discord_blacklist')
  let g:discord_blacklist = []
endif
if !exists('g:discord_trace')
  let g:discord_trace = []
endif
if !exists('g:discord_fts_whitelist')
  let g:discord_fts_whitelist = [
        \'asm',
        \'c',
        \'chef',
        \'coffee',
        \'cpp',
        \'crystal',
        \'cs',
        \'css',
        \'d',
        \'dart',
        \'diff',
        \'dockerfile',
        \'elixir',
        \'erlang',
        \'git',
        \'gitconfig',
        \'gitignore',
        \'go',
        \'haskell',
        \'html',
        \'javascript',
        \'json',
        \'jsx',
        \'kotlin',
        \'lang_c',
        \'lang_d',
        \'less',
        \'lua',
        \'markdown',
        \'neovim',
        \'nix',
        \'perl',
        \'php',
        \'python',
        \'ruby',
        \'rust',
        \'sass',
        \'scss',
        \'swagger',
        \'tex',
        \'tf',
        \'vim',
        \'xml',
        \'yaml',
        \]
endif
if !exists('g:discord_fts_blacklist')
  let g:discord_fts_blacklist = ['help', 'nerdtree']
endif
