#!/bin/bash

function ctrl_c() {
    echo -e "\n\n[+] Ending script ... \n"
    exit 1
}

trap ctrl_c INT

function decompress() {
    echo -e "[*]Decompressing file... "
    sleep 2
    filename=$1
    toDecompress=$(7z l $filename | tail -n 3 | head -n 1 | awk 'NF{print $NF}')
    7z x $filename &>/dev/null

    while [ "$toDecompress" ]; do
        echo -e "[+] File decompressed: $toDecompress"
        7z x "$toDecompress" &>/dev/null
        toDecompress=$(7z l "$toDecompress" 2>/dev/null | tail -n 3 | head -n 1 | awk 'NF{print $NF}')
    done
}

function compress() {
    echo "place holder"
}

function main() {
    echo -e "\n\033[1;32m"
    cat << "EOF"
  ██████╗ ██████╗ ███╗   ███╗██████╗ 
 ██╔════╝██╔═══██╗████╗ ████║██╔══██╗
 ██║     ██║   ██║██╔████╔██║██████╔╝
 ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ 
 ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     
  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     
   [ Compress / Decompress Tool v1.0 ]
EOF
    echo -e "\033[0m"
    read -p "Name of the file to process: " filename
    read -p "Would you like to (D)ecompress or (C)ompress a file[D/C]: " chose
    if [[ "$chose" == "D" ]]; then
        decompress $filename
    elif [[ "$chose" == "C" ]]; then
        compress
    else
        echo -e "[!]You must chose between (D)ecompress or (C)ompress"
    fi
}

main