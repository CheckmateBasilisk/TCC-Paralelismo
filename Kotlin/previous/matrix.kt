//from tutorialspoint on mutable vs immutable collections:
// (...) Kotlin system does not represent any specific difference in them.
// changing immutable variables seems to get caught in compile time


import kotlin.random.Random
import kotlin.system.measureTimeMillis

fun main(args: Array<String>) {
    val n : Int = 3000 // nxn matrices
    val nThreads: Int = args[0].toInt() // arg[0] isnt the program name, it is the actual first argument
    val min = -10
    val max = 10
    val m1 : Array<IntArray> = getRandomMatrix(n, min, max+1) //randomMatrix generates in [min, max[
    val m2 : Array<IntArray> = getRandomMatrix(n, min, max+1)
    var result : Array<IntArray> = Array(n) { IntArray(n) { 0 } }//matrix filled with 0s

    val elapsed = measureTimeMillis {
        if (nThreads == 0) {
                matrix(m1, m2, result)
            } else {
                matrix_thread(m1, m2, result, nThreads)
            }
    }
    println("${elapsed.toDouble()/1000}") //elapsed time must be in seconds
}


fun getRandomMatrix(n:Int , min: Int, max: Int): Array<IntArray> {
    val m = Array(n) { IntArray(n) { Random.nextInt(min, max) } } //creates an array of IntArrays

    return m; //immutability ends with scope?
}

fun matrix(m1: Array<IntArray>, m2: Array<IntArray>, result: Array<IntArray>) {
    for (i in 0..result.size-1) { //kotlin ranges are inclusive!
        for (j in 0..result[i].size-1) {
            for (k in 0..result.size-1) {
                result[i][j] += m1[i][k] * m2[k][j]
            }
        }
    }

}

fun matrix_thread(m1: Array<IntArray>, m2: Array<IntArray>, result: Array<IntArray>, nThreads: Int){
    for (i in 0..result.size-1) { //kotlin ranges are inclusive!
        for (j in 0..result[i].size-1) {
            for (k in 0..result.size-1) {
                result[i][j] += m1[i][k] * m2[k][j]
            }
        }
    }
}

fun printMatrix(m : Array<IntArray>){
    for (i in m.indices) {
        println(m[i].contentToString())
    }
}
