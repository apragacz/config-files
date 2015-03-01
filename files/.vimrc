set background=dark
set autoindent
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4
autocmd FileType c,cpp,java,php,js,python,xml autocmd BufWritePre <buffer> :call setline(1,map(getline(1,"$"),'substitute(v:val,"\\s\\+$","","")'))
filetype plugin indent on
syntax on
set mouse=a  
set virtualedit=onemore
set history=1000
set cursorline
if has('cmdline_info')
    set ruler
    set rulerformat=%30(%=\:b%n%y%m%r%w\ %l,%c%V\ %P%)
    set showcmd  
endif
