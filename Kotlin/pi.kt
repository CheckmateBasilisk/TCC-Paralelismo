package pi

import kotlin.math.pow
import kotlin.system.measureTimeMillis

fun main(args: Array<String>) {
    val nIter : Int = 100_000_000 // 10m iterations
    val nThreads : Int = args[0].toInt() // arg[0] isnt the program name, it is the actual first argument

    val elapsed = measureTimeMillis {
        if (nThreads == 0) {
                pi(nIter)
            } else {
                pi_thread_coroutine(nIter, nThreads)
            }
    }

    println("${elapsed.toDouble()/1000}") //elapsed time must be in seconds


}

fun pi(maxIter: Int) : Double {
    var result: Double  = 0.0

    for (i in 0..maxIter) {
        result += 4 * (-1.0).pow(i) * 1/(i*2+1)
    }

    return result
}

// paralelism implemented via coroutines
// computes pi partially
fun pi_thread_coroutine(maxIter: Int, nThreads: Int) : Double {

    for (t in 0..nThreads-1) {


    }

    return result
}
