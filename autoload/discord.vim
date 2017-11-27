function! discord#GetClientID()
  if exists('g:discord_clientid')
    return g:discord_clientid
  else
    return '383069395896762369'
  endif
endfunction

" Stolen from https://github.com/w0rp/ale/blob/master/autoload/ale/path.vim#L46
function! discord#FindNearestDir(buffer, directory_name)
  let l:buffer_filename = fnamemodify(bufname(a:buffer), ':p')

  let l:relative_path = finddir(a:directory_name, l:buffer_filename . ';')

  if !empty(l:relative_path)
    return fnamemodify(l:relative_path, ':p')
  endif

  return ''
endfunction

function! discord#GetProjectDir(buffer)
  for l:vcs_dir in ['.git', '.hg']
    let l:dir = discord#FindNearestDir(a:buffer, l:vcs_dir)
    if !empty(l:dir)
      return fnamemodify(l:dir, ':h:h')
    endif
  endfor
  return ''
endfunction
