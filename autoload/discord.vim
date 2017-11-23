function! discord#get_clientid()
  if exists('g:discord_clientid')
    return g:discord_clientid
  else
    return '383069395896762369'
  endif
endfunction
