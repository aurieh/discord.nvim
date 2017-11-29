if !has('nvim')
  echoerr 'This plugin requires Neovim'
endif
if !has('timers')
  echoerr 'This plugin requires +timers build option'
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
let g:discord_trace = []
