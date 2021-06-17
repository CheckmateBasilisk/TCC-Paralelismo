#!/bin/bash

# path to output files for every program
OUTPUT_DIR=./output

# path to dir with executables/scripts
# like [application].py
PYTHON_DIR=./Python
RUST_DIR=./Rust
HASKELL_DIR=./Haskell
GO_DIR=./Go
KOTLIN_DIR=./Kotlin

METHOD=(single thread)
APPLICATION=(pi matrix)
LANGUAGE=(python rust haskell go kotlin)
THREADS=(0 1 2 3 4) # 0 threads means a non-paralelized application

if [ $1 = "clear" ] # clears output files
then
    rm $OUTPUT_DIR/*

    for T in ${THREADS[@]}
    do
        for A in ${APPLICATION[@]}
        do
            touch "${OUTPUT_DIR}/python_${A}_${T}threads.out"
            touch "${OUTPUT_DIR}/go_${A}_${T}threads.out"
            touch "${OUTPUT_DIR}/rust_${A}_${T}threads.out"
            touch "${OUTPUT_DIR}/haskell_${A}_${T}threads.out"
            touch "${OUTPUT_DIR}/kotlin_${A}_${T}threads.out"
        done
    done
else
    for T in ${THREADS[@]}
    do
        for A in ${APPLICATION[@]}
        do
            #echo "${L}_${A}-${T}threads.out"
            python3 $PYTHON_DIR/${A}.py ${T} >> ${OUTPUT_DIR}/python_${A}_${T}threads.out

            #echo "$GO_DIR/${A}.go ${T} >> ${OUTPUT_DIR}/go_${A}_${T}threads.out"
            #echo "$RUST_DIR/${A}.rs ${T} >> ${OUTPUT_DIR}/rust_${A}_${T}threads.out"
            #echo "$HASKELL_DIR/${A}.hs ${T} >> ${OUTPUT_DIR}/haskell_${A}_${T}threads.out"
            #echo "$KOTLIN_DIR/${A}.ktl ${T} >> ${OUTPUT_DIR}/kotlin_${A}_${T}threads.out"
            

        done
    done

fi
