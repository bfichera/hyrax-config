#
# ~/.bashrc
#

set -o vi

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
export GPG_TTY=$(tty)

set editor=vim

alias cdproj='ls $HOME/data/projects'
alias mv='mv -vi'
alias rm='rm -v'
alias grep='grep --color'
alias office='ssh -XY -p 13802 bfichera@bfichera-office-arch.mit.edu'
alias cloud='ssh -o TCPKeepAlive=yes -o ServerAliveCountMax=5760 -o ServerAliveInterval=15 bfichera@txe1-login.mit.edu'
alias config='/usr/bin/git --git-dir=$HOME/.cfg --work-tree=$HOME'
alias cdshg='cd $HOME/data/projects/shg/SHG_cubr2'
alias cdshgpy='cd /home/bfichera/data/projects/shgpy'
alias freecad='exec=/usr/bin/env QT_SCALE_FACTOR=0.6 /usr/bin/freecad'
alias zoom='exec=/usr/bin/env QT_SCALE_FACTOR=0.5 /usr/bin/zoom'
alias cdproj='cd /home/bfichera/data/projects'
alias wifi-bos='sudo netctl start wlan0-BESTWIFIPOGGERS-5G'
alias wifi-home='sudo netctl start wlan0-PHOTOEMITTER'
alias wifi-work='sudo netctl start "wlan0-MIT SECURE"'
alias wifi-cami='sudo netctl start "wlan0-johnturner"'
alias wifi-chic='sudo netctl start "wlan0-eduroam"'
alias wifi-bora='sudo netctl start wlan0-BEREHLA_24G'
alias cdcmb='cd /home/bfichera/data/projects/CMB'
alias cdcam='cd /home/bfichera/data/projects/grocery_covenants/data/acquire'
alias cdpap='cd /home/bfichera/data/projects/manuscripts/paper_CaMn2Bi2/src/tex'
alias cdpape='cd /home/bfichera/data/projects/manuscripts/paper_CuBr2/src'
alias cdtas2='cd /home/bfichera/data/projects/manuscripts/NCtas2'
alias icat='kitty +kitten icat'
alias cdraman='cd $HOME/data/projects/raman/RAMAN_camn2bi2/polarized/twomagnon'
alias chess='ssh bfichera@lnx201.classe.cornell.edu'
alias saclavpn='sudo openconnect https://hpc.spring8.or.jp'
alias sacla='ssh bfichera@xhpcfep.hpc.spring8.or.jp'
alias saclascp='scp bfichera@xhpcfep.hpc.spring8.or.jp'
alias evince='evince-and-exit'
alias cdthes='cd $HOME/data/projects/thesis'
alias v='source venv/bin/activate'
alias d='deactivate'
alias z='zathura-and-exit'
alias s='maim -s --format=png /dev/stdout | xclip -selection clipboard -t image/png -i'

alias ls='ls --color=auto'

. /usr/share/LS_COLORS/dircolors.sh

TSET='\[\033[38;5;122m\]'
HOST='@\h '
parse_git_branch () { git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'; }
LOCATION='\[\033[38;5;182m\]`pwd | sed "s#\(/[^/]\{1,\}/[^/]\{1,\}/[^/]\{1,\}/\).*\(/[^/]\{1,\}/[^/]\{1,\}\)/\{0,1\}#\1...\2#g"`'
BRANCH=' \[\033[38;5;229m\]$(parse_git_branch)\[\033[00m\]\$ '
PS1=$TSET$USER$HOST$LOCATION$BRANCH

eval "$(jump shell)"

clear
