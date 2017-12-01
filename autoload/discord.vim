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
  for l:vcs_dir in ['.git', '.hg', '.bzr', '_darcs', '.svn']
    let l:dir = discord#FindNearestDir(a:buffer, l:vcs_dir)
    if !empty(l:dir)
      return fnamemodify(l:dir, ':h:h')
    endif
  endfor
  return ''
endfunction

function! discord#LogDebug(message, trace)
  call add(g:discord_trace, a:trace)
  if g:discord_log_debug
    echomsg '[discord] ' . a:message
  endif
endfunction

function! discord#LogWarn(message, trace)
  call add(g:discord_trace, a:trace)
  echohl WarningMsg | echomsg '[discord] ' . a:message | echohl None
endfunction

function! discord#LogError(message, trace)
  call add(g:discord_trace, a:trace)
  echohl ErrorMsg | echomsg '[discord] ' . a:message | echohl None
endfunction
