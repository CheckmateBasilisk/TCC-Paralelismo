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
    const maxIter = 10_000_000 //10m iterations
    var nThreads, _ = strconv.Atoi(os.Args[1])

    start := time.Now()

    if nThreads == 0 {
        fmt.Println(pi(maxIter))
    } else {
        // runtime.GOMAXPROCS(nThreads) //limits the nr of actual OS threads
        fmt.Println(piThread(maxIter, nThreads))
    }

    elapsedTime := time.Since(start)
    fmt.Println(elapsedTime)

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
        // computes pi partially
        // outputs the result in the channel
        go func(start int, end int, ch chan float64) {
            var i int = 0
            var r float64 = 0
            for i = start; i < end; i++ {
                r += 4.0 * math.Pow(-1, float64(i)) * 1/(float64(i)*2+1)
            }

            ch <- r
        }(int(i*maxIter/nThreads), int((i+1)*maxIter/nThreads), ch)
    }

    //joining threads
    for i := 0; i < nThreads; i++ {
        result += <-ch
    }

    close(ch) // needs closing?
    return result
}


// auxiliary function to piThread
// given start, end, partially computes pi using the Leibniz series
// result output into the result channel
func piThread_aux(start int, end int,result chan float64){

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

// computes pi partially (Leibniz' Formula)
// starts at start and goes to maxIter
// if start == 0, it computes pi correctly
func piPart(start int, maxIter int) float64 {
    var result float64 = 0

    return result
}


func piThreaded(maxIter int, nThreads int) float64 {
    var result float64 = 0

    return result
}
