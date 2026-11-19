#!/usr/bin/env bash
# exit codes 0-success, 1-script error, 2-user error, 4-help

help_and_exit(){
  cat 1>&2 << EOF
${BRIGHT}fw_nc.sh${NOCOLOR}: firewall netcat

Open port(s) in the firewall, run netcat, and then remove the firewall rule.

Script gets port and proto from netcat statement, no special options, just use
netcat syntax.

	${BRIGHT}USAGE${NOCOLOR}:
	fw_nc.sh <netcat statement>
EOF
  exit 4
}

BRIGHT=$(tput bold)
NOCOLOR=$(tput sgr0) #reset to default colors
BRIGHT_RED=$(tput setaf 1;tput bold)
BRIGHT_YELLOW=$(tput setaf 3;tput bold)
BRIGHT_CYAN=$(tput setaf 6;tput bold)

exit_with_error(){
  echo 1>&2 "${BRIGHT}fw_nc.sh.sh: ${BRIGHT_RED}ERROR${NOCOLOR}: ${2}"
  exit ${1
}
message(){
  echo "fw_nc.sh: ${@}"
}

check_sudo(){
  # Check if this script can run sudo correctly. uses as_root, see below
  if [ ${UID} -eq 0 ];then
    ROOT_METHOD="uid"
   # TODO: FIX Polkit support
   #elif [[ ! -z $DISPLAY && $(tty) = /dev/pts/* ]];then
   # ROOT_METHOD="pkexec"
   elif [ $(sudo whoami ) == "root" ];then
    ROOT_METHOD="sudo"
   else
    exit_with_error 4 "Cannot gain root! This program needs root to work Exiting..."
  fi
  # one last check
  [ $( as_root whoami ) != "root" ] && exit_with_error 4 "Cannot gain root! This program needs root to work Exiting..."
}
as_root(){
  # execute a command as root.
  case $ROOT_METHOD in
   sudo)
    sudo ${@}
    ;;
   polkit)
    pkexec ${@}
    ;;
   uid)
    ${@}
    ;;
  esac
}
check_nc_opts() {
  CHAIN="OUTPUT"
  PROTO="tcp"
  PORT=""
  local parms=""
  while [ ! -z "$1" ];do
    item="${1}"
    case ${item} in
     -l)
      PORT=${2}
      CHAIN="INPUT"
      ;;
     -u)
      PROTO="udp"
      ;;
     -*)
      shift
      continue
      ;;
     *)
      parms+=${item}
      ;;
    esac
    shift
  done
  [ -z "${parms}" ] && return
  set ${parms}
  [ -z ${PORT} ] && PORT=${2}
}

remove_rule_and_exit() {
  as_root iptables -D ${CHAIN} -m ${PROTO} -p ${PROTO} --dport ${PORT} -j ACCEPT
  exit
}

main() {
  # Sanity Check
  [ -z $1 ] && help_and_exit
  [ $1 == "--help" ] && help_and_exit
  [ -z $PORT ] && exit_with_error 2 "no such port"
  check_sudo
  as_root iptables -I ${CHAIN} -m ${PROTO} -p ${PROTO} --dport ${PORT} -j ACCEPT
  trap remove_rule_and_exit 1 2 3 9 15
  nc ${@}
  remove_rule_and_exit
}

check_nc_opts "${@}"
main "${@}"


