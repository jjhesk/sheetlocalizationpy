#!/bin/sh

gitpush(){
    git add .
    #git remote add origin https://gitee.com/jjhoc/vue-tronlink.git
    git commit -m "package updates related items. please check in commit details"
    git push
}

# Accepts a version string and prints it incremented by one.
# Usage: increment_version <version> [<position>] [<leftmost>]
increment_version() {
  declare -a part=( ${1//\./ } )
  declare    new
  declare -i carry=1

  for (( CNTR=${#part[@]}-1; CNTR>=0; CNTR-=1 )); do
    len=${#part[CNTR]}
    new=$((part[CNTR]+carry))
    [ ${#new} -gt $len ] && carry=1 || carry=0
    [ $CNTR -gt 0 ] && part[CNTR]=${new: -len} || part[CNTR]=${new}
  done
  new="${part[*]}"
   if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${new// /.}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "${new// /.}"
    elif [[ "$OSTYPE" == "cygwin" ]]; then
        echo "not correct system - cygwin detected"
        exit
    fi

}