package main

import (
    "fmt" //for printing to stdout
//    "sync" //for the wait groups
)

func main() {
    c := make(chan int)
    threads := 10

    for i := 0; i < threads; i++ {
        go func(i int, c chan int) {
            c <- i*2

        }(i, c)
    }

    // nr of reads == nr of writes to channel guarantees no deadlock...
    for i := 0; i < threads; i++ {
        fmt.Println(<- c)
    }




}
