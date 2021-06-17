#!/bin/sh

OUTPUT_DIR=./output
METHOD=single

#output files with the execution times
PYTHON_OUTPUT_SINGLE=$OUTPUT_DIR/python_single
PYTHON_OUTPUT_THREADS=$OUTPUT_DIR/python_thread
PYTHON_OUTPUT_PROCESSES=$OUTPUT_DIR/python_process

RUST_OUTPUT=$OUTPUT_DIR/rust
GO_OUTPUT=$OUTPUT_DIR/go
KOTLIN_OUTPUT=$OUTPUT_DIR/kotlin
HASKELL_OUTPUT=$OUTPUT_DIR/haskell

if [ $1 = "clear" ]
then
    rm $OUTPUT_DIR/*
fi

touch $PYTHON_OUTPUT_SINGLE
touch $PYTHON_OUTPUT_THREADS
touch $PYTHON_OUTPUT_PROCESSES

THREAD_COUNT=0
MAX_THREAD=4
while [ $THREAD_COUNT -lt $MAX_THREAD ]
do
    ITER_COUNT=0
    MAX_ITER=3
    while [ $ITER_COUNT -lt $MAX_ITER ]
    do
        echo "$ITER_COUNT / $MAX_ITER"

        python3 ./Python/runMe.py pi single THREAD_COUNT >> $PYTHON_OUTPUT_THREADS
        python3 ./Python/runMe.py pi thread >> $PYTHON_OUTPUT_THREADS
        python3 ./Python/runMe.py pi process >> $PYTHON_OUTPUT_PROCESSES

        python3 ./Python/runMe.py matrix single >> $PYTHON_OUTPUT_THREADS
        python3 ./Python/runMe.py matrix thread >> $PYTHON_OUTPUT_THREADS
        python3 ./Python/runMe.py matrix process >> $PYTHON_OUTPUT_PROCESSES

        ITER_COUNT=`expr $ITER_COUNT + 1`
    done
done
