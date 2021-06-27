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

N_RUNS=5

if [ $# -gt 0 ] # clears output files
then
    if [ $1 = "clear" ] # looks ugly. Will work for now
    then
        rm $OUTPUT_DIR/*

        for T in ${THREADS[@]}
        do
            for A in ${APPLICATION[@]}
            do
                touch "${OUTPUT_DIR}/python_threadpool_${A}_${T}threads.out"
                touch "${OUTPUT_DIR}/python_processpool_${A}_${T}threads.out"
                touch "${OUTPUT_DIR}/go_${A}_${T}threads.out"
                touch "${OUTPUT_DIR}/rust_${A}_${T}threads.out"
                touch "${OUTPUT_DIR}/haskell_${A}_${T}threads.out"
                touch "${OUTPUT_DIR}/kotlin_${A}_${T}threads.out"
            done
        done
    else
        echo "usage: ./manager [clear]"
    fi
else
    RUN=0
    while [ $RUN -lt $N_RUNS ]
    do
        RUN=`expr $RUN + 1`;
        echo ""
        #echo $RUN/$N_RUNS
        for T in ${THREADS[@]}
        do
            for A in ${APPLICATION[@]}
            do
                echo "Run $RUN/$N_RUNS - $A, $T threads"
                #echo "${L}_${A}-${T}threads.out"
                python3 $PYTHON_DIR/${A}.py ${T} process >> ${OUTPUT_DIR}/python_threadpool_${A}_${T}threads.out
                python3 $PYTHON_DIR/${A}.py ${T} thread >> ${OUTPUT_DIR}/python_processpool_${A}_${T}threads.out
                echo -e "\tPython DONE"
                # ./Go/pi/pi.exe nthreads
                $GO_DIR/${A}/${A} ${T}  >> ${OUTPUT_DIR}/go_${A}_${T}threads.out
                echo -e "\tGo DONE"
                #echo "$RUST_DIR/${A}.rs ${T} >> ${OUTPUT_DIR}/rust_${A}_${T}threads.out"
                #echo "$HASKELL_DIR/${A}.hs ${T} >> ${OUTPUT_DIR}/haskell_${A}_${T}threads.out"
                #echo "$KOTLIN_DIR/${A}.ktl ${T} >> ${OUTPUT_DIR}/kotlin_${A}_${T}threads.out"


            done
        done
    done

fi
