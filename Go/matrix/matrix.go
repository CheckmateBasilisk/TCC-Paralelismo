package main

import(
    //"math" // for power
    "math/rand" //for random nr generation
    "fmt" //for printing to stdout
    "time" //for counting elapsed time
    "os" //for acess to params
    "strconv" //for converting str to int

    "sync" //for waitgroups
)

func main() {
    var nThreads, _ = strconv.Atoi(os.Args[1])
    const n = 1000 // matrix size
    const minVal int =  -10
    const maxVal int =  10

    // innitializing matrices
    // this code will use shared memory space
    m1 := getRandomMatrix(n, minVal, maxVal)
    m2 := getRandomMatrix(n, minVal, maxVal)

    result := make([][]int, n)
    for i := range result {
        result[i] = make([]int, n)
    }

    start := time.Now()

    if nThreads == 0 {
        matrixMult(n, m1, m2, result)
    } else {
        // runtime.GOMAXPROCS(nThreads) //limits the nr of actual OS threads
        matrixThread(n, m1, m2, result, nThreads)
    }

    elapsedTime := time.Since(start)
    fmt.Println(elapsedTime.Seconds())

    //printMatrix(n,result)

    return
}

func matrixThread(n int, m1 [][]int ,m2 [][]int, result [][]int, nThreads int) {
    var wg sync.WaitGroup

    //spawning threads
    for i := 0; i < nThreads; i++ {
        // adds to the wait group
        wg.Add(1)
        // computes m1 x m2 partially in goroutines
        // outputs the result in shared memory matrix result
        // must pass the waitGroup to it so it warns the outside scope when it finishes
        go func(start int, end int, wg *sync.WaitGroup){
            for i := 0; i < end; i++ {
                for j := range result[i] {
                    for k := range result[i]{
                        result[i][j] += m1[i][k] * m2[k][j]
                    }
                }
            }
            wg.Done() // warns the outside scope the thread finished, decreases 1 in the internal wg counter, similar to a semaphore.
        }(int(i*n/nThreads), int((i+1)*n/nThreads), &wg)
    }

	wg.Wait() // wait until all threads finished
    //return
}


func matrixMult(n int, m1 [][]int ,m2 [][]int, result [][]int) {
    for i := range result {
        for j := range result[i] {
            for k := range result[i]{
                result[i][j] += m1[i][k] * m2[k][j]
            }
        }
    }

    //return
}


func getRandomMatrix(n int, minVal int, maxVal int) [][]int{
    rand.Seed(time.Now().UTC().UnixNano())
    //rand.Seed(1)

    m := make([][]int, n)
    for i := range m {
        m[i] = make([]int, n)
        for j := range m[i] {
            m[i][j] = rand.Intn(20) - 10 //TODO: hardcoding is bad but i'm not dealing with this right now...
        }
    }

    return m
}

func printMatrix(n int, m [][]int) {
    for i := range m {
        for j:= range m[i] {
            fmt.Printf("%v ", m[i][j])
        }
        fmt.Printf("\n")
    }
}
