#!/bin/bash

# path to output files for every program
OUTPUT_DIR=./output

# path to dir with executables/scripts
# like [application].py
PYTHON_DIR=./Python
#   python pi runs with n=10_000_000
#   python matrix runs with n=300
GO_DIR=./Go
#   go pi runs with n=10_000_000
#   go matrix runs with n=300
RUST_DIR=./Rust
#   rust pi runs with n=10_000_000
#   rust matrix runs with n=300
KOTLIN_DIR=./Kotlin
#   kotlin pi runs with n=10_000_000
#   kotlin matrix runs with n=300
HASKELL_DIR=./Haskell
#   haskell pi runs with n=10_000_000
#   haskell matrix runs with n=300

#APPLICATION=(pi matrix)
APPLICATION=(pi)
LANGUAGE=(python go rust kotlin haskell)
THREADS=(0 1 2 3 4) # 0 threads means a non-paralelized application

N_RUNS=3

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

                # python3 ./Python/pi/pi.py nthreads process/thread
                python3 $PYTHON_DIR/${A}.py ${T} process >> ${OUTPUT_DIR}/python_threadpool_${A}_${T}threads.out
                python3 $PYTHON_DIR/${A}.py ${T} thread >> ${OUTPUT_DIR}/python_processpool_${A}_${T}threads.out
                echo -e "\tPython DONE"

                # TODO: talvez eu deva fazer go run ./Go/pi/pi.go pra garantir que a coisa compila. Eu chequei e não tem flags de otimização adicional tbm
                # ./Go/pi/pi.exe nthreads
                $GO_DIR/${A}/${A} ${T}  >> ${OUTPUT_DIR}/go_${A}_${T}threads.out

                echo -e "\tGo DONE"
                # cargo run --manifest-path ./Rust/pi/Cargo.toml --release 0
                #   manifest path is the path to the Cargo.toml which contains the dependency list etc.
                #   --release orders it to build run an optimized version
                #   -q do it quietly
                cargo run --manifest-path $RUST_DIR/${A}/Cargo.toml --release -q ${T} >> ${OUTPUT_DIR}/rust_${A}_${T}threads.out
                echo -e "\tRust DONE"

                #echo "$KOTLIN_DIR/${A}.ktl ${T} >> ${OUTPUT_DIR}/kotlin_${A}_${T}threads.out"
                #echo "$HASKELL_DIR/${A}.hs ${T} >> ${OUTPUT_DIR}/haskell_${A}_${T}threads.out"


            done
        done
    done

fi
