package main

import(
    "math" // for power
    "fmt" //for printing to stdout
    "time" //for counting elapsed time
    "os" //for acess to params
    "strconv" //for converting str to int
)

//TODO: pesquisar sobre select

func main() {
    const maxIter = 1_000_000_000 //1b iterations
    var nThreads, _ = strconv.Atoi(os.Args[1])

    start := time.Now()

    if nThreads == 0 {
        pi(maxIter)
    } else {
        // runtime.GOMAXPROCS(nThreads) //limits the nr of actual OS threads
        piThread(maxIter, nThreads)
    }

    elapsedTime := time.Since(start)
    fmt.Println(elapsedTime.Seconds())

    return
}

// given the number of max_iterations
// computes pi using 'max_iterations' terms of a series (Leibniz's Formula)
// creates nThreads goroutines and joins them safely
// 10 million max_iterations, wields 6 digit-precise pi
func piThread(maxIter int, nThreads int) float64{
    ch := make(chan float64) // channels are the most natural way of getting values out of goroutines
    var result float64 = 0

    //spawning threads
    for i := 0; i < nThreads; i++ {
        // computes pi partially in goroutines
        // outputs the result in the channel ch
        go func(start int, end int, ch chan float64) {
            var i int = 0
            var r float64 = 0
            for i = start; i < end; i++ {
                r += 4.0 * math.Pow(-1, float64(i)) * 1/(float64(i)*2+1)
            }
            // writing to channels is a blocking operation and it waits until someone reads from said channel
            // many writes to a channel creates a waiting queue but does not guarantee order, as expected
            ch <- r
        }(int(i*maxIter/nThreads), int((i+1)*maxIter/nThreads), ch)
    }

    //joining threads
    for i := 0; i < nThreads; i++ {
        // reading from channel is a blocking operation and it waits for a write
        // the number of reads MUST be the same nr of writes, since i'm not using a buffered channel or wait groups
        result += <-ch
    }

    close(ch) // needs closing?
    return result
}

// given the number of max_iterations
// computes pi using 'max_iterations' terms of a series (Leibniz's Formula)
// 10 million max_iterations, wields 6 digit-precise pi
func pi(maxIter int) float64 {
    var result float64 = 0

    var i int = 0
    for i = 0; i < maxIter; i++ {
        result += 4.0 * math.Pow(-1, float64(i)) * 1/(float64(i)*2+1)//geez, to type coersion then? not ever some kind of numeric supertype?
    }

    return result
}
