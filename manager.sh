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
#APPLICATION=(pi)
APPLICATION=(matrix)
LANGUAGE=(python go rust kotlin)
THREADS=(0 1 2 3 6 10 100) # 0 threads means a non-paralelized application
#THREADS=(100) # 0 threads means a non-paralelized application

N_RUNS=30

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
                #touch "${OUTPUT_DIR}/haskell_${A}_${T}threads.out"
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
                #python3 $PYTHON_DIR/${A}.py ${T} process >> ${OUTPUT_DIR}/python_threadpool_${A}_${T}threads.out
                #python3 $PYTHON_DIR/${A}.py ${T} thread >> ${OUTPUT_DIR}/python_processpool_${A}_${T}threads.out
                #echo -e "\tPython DONE"

                # ./Go/pi/pi.exe nthreads
                # TODO: talvez eu deva fazer go run ./Go/pi/pi.go pra garantir que a coisa compila. Eu chequei e n??o tem flags de otimiza????o adicional tbm
                #go run $GO_DIR/${A}/${A}.go ${T}  >> ${OUTPUT_DIR}/go_${A}_${T}threads.out
                #echo -e "\tGo DONE"

                # cargo run --manifest-path ./Rust/pi/Cargo.toml --release 0
                #   manifest path is the path to the Cargo.toml which contains the dependency list etc.
                #   --release orders it to build run an optimized version
                #   -q do it quietly
#                cargo run --manifest-path $RUST_DIR/${A}/Cargo.toml --release -q ${T} >> ${OUTPUT_DIR}/rust_${A}_${T}threads.out
#                echo -e "\tRust DONE"

                # java -jar ./Kotlin/pi.jar
                # echo "java -jar $KOTLIN_DIR/${A}.ktl ${T} >> ${OUTPUT_DIR}/kotlin_${A}_${T}threads.out"
                # since kotlin is such a corporate bitch, gradle is necessary. Otherwise IntelliJ is needed and I'm not installing a colossal IDE just for this...

                # gradle run -p ./Kotlin/pi --args="nthreads" -q
                #   gradle is the project management tool needed to use external packages with kotlin
                #   run builds and runs the project
                #   -p defines is the project directory, if omitted . is the default
                #   --args="" is needed to pass arguments to the program
                #   -q is to execute quietly, supressing gradle output and just showing the app output

                gradle run -p $KOTLIN_DIR/${A} --args="${T}" -q >> ${OUTPUT_DIR}/kotlin_${A}_${T}threads.out
                # tive que fazer umas bizarrices pra funcionar.
                #   adicionando depend??ncias: no arquivo ./app/build.gradle.kts , adicionar na se????o dependencies{} implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.5.1")
                #   me livrar dos arquivos para testes (que pararam de funcionar com a adi????o da depend??ncia, nem ideia de pq): arquivo ./app/src/test/kotlin/pi/AppTest.kt, basicamente tdo o c??digo
                echo -e "\tKotlin DONE"


                #echo "$HASKELL_DIR/${A}.hs ${T} >> ${OUTPUT_DIR}/haskell_${A}_${T}threads.out"


            done
        done
    done
fi

# build commands
# kotlinc $KOTLIN_DIR/matrix.kt -d $KOTLIN_DIR/matrix.jar -include-runtime
# kotlinc $KOTLIN_DIR/pi.kt -d $KOTLIN_DIR/pi.jar -include-runtime


# compilation commands
# python : not needed. Python is interpreted. Just run using python3 script.py
# rust : cargo build --release (inside proj directory or using --manifest-path ./path_to_toml_file)
# go : go build source.go
# Kotlin: kotlinc source.kt -include-runtime -d out.jar  (builda a .jar file from the outputs, include runtime akin to static compilation but it is an application, not a module)
# Kotlin: gradle build -p ./project_dir
# haskell : ??
