package main

import (
    "fmt" //for printing to stdout
    "math/rand"
    //"math"
    //"sync" //for the wait groups
    "time"
)

func main() {
    //var m [][]int
    n := 3
    const minVal int =  -10
    const maxVal int =  10
    rand.Seed(time.Now().UTC().UnixNano())

    m := getRandomMatrix(n, minVal, maxVal)
    printDestroyMatrix(m, n)
}

func printDestroyMatrix(m [][]int, n int) {
    for i := range m {
        for j:= range m[i] {
            fmt.Printf("%v ", m[i][j])
            m[i][j] = 0
        }
        fmt.Printf("\n")
    }
}


func getRandomMatrix(n int, minVal int, maxVal int) [][]int{
    rand.Seed(time.Now().UTC().UnixNano())

    m := make([][]int, n)
    for i := range m {
        m[i] = make([]int, n)
        for j := range m[i] {
            m[i][j] = rand.Intn(20) - 10 //TODO: hardcoding is bad but i'm not dealing with this right now...
        }
    }

    return m
}
