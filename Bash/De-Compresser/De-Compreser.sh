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

    exit 0
}

function compress() {
    read -p "[?] How may times do you want to compress the file? " n_comp
    
    if [[ $var =~ ^[0-9]+$ ]]; then
        cat << 'EOF'
        7z a file.7z carpeta/         # 7z    -> supports folders
        7z a -tzip file.zip carpeta/  # zip   -> supports folders
        7z a -tgzip file.gz archivo   # gzip  -> single file only
        7z a -tbzip2 file.bz2 archivo # bzip2 -> single file only
        7z a -ttar file.tar carpeta/  # tar   -> supports folders
        7z a -twim file.wim carpeta/  # wim   -> supports folders
EOF
        while [[ $n_comp < 0 ]]; do
            read -p "[?] Extension to compress the file: " exten
            read -p "[?] Name to compress the file: " filecomp
            if [[ "$exten" == 7z]]; then
                7z a $filecomp.7z $filename
            else
                7z a -t$exten $filecomp.$exten $filename
            fi
        done

        exit 0
    else
        echo -e "[!] Not a number"
        exit 1
    fi
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
    read -p "Name of the file to process(including extension): " filename
    read -p "Would you like to (D)ecompress or (C)ompress a file[D/C]: " chose
    if [[ "$chose" == "D" ]]; then
        decompress $filename
    elif [[ "$chose" == "C" ]]; then
        compress
    else
        echo -e "[!]You must chose between (D)ecompress or (C)ompress"
        exit 1
    fi
}

main