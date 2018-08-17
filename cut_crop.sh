#!/bin/bash

pdfsize() {
    a=$(pdfinfo -box ${1} | grep "MediaBox")
    echo ${a#*:}
}

createBox() {
    x1=${3}
    x2=${7}
    y1=${4}
    y2=${8}
    deltay=$(echo ${y1} - ${y2} | bc )
    deltax=$(echo ${x1} - ${x2} | bc )
    if [[ ${deltax} = *-* ]]
    then
        deltax=0
    fi
    if [[ ${deltay} = *-* ]]
    then
        deltay=0
    fi
    echo "${deltax} 0 0 ${deltay}"
}

pdfcropy() {
    file=${1}
    box=${2}
    echo "Adding margins: " ${box}
    pdfcrop --margins "${box}" ${file} ${file}
}
pdfclip() {
    file=${1}
    pdfcrop --clip ${file} ${file}
}


do_all() {
    larger=${1}
    smaller=${2}

    if [[ ${3} != *noclip* ]] 
    then
        pdfclip ${larger}
        pdfclip ${smaller}
    fi

    size_l=$(pdfsize ${larger})
    size_s=$(pdfsize ${smaller})
    echo "Size L :" ${size_l}
    echo "Size S :" ${size_s}

    box=$(createBox ${size_l} ${size_s})

    pdfcropy ${smaller} "${box}"
}

do_all bigger.pdf smaller.pdf

