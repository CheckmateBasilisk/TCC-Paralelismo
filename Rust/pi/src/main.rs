// to count time
use std::time::Instant;
use std::env;
use std::thread;//spawning threads
//use std::sync::mpsc;//using channels

fn main() {
    let max_iter = 10_000_000;

    let args: Vec<String> = env::args().collect();//geting args from cmd line
    let n_threads:usize = args[1].parse::<i32>().unwrap() as usize;//converting arg['nthreads'] to uint
    //WILL NOT DEAL WITH MISUSE!!

    let result: f64;
    let time = Instant::now();
    if n_threads == 0 {
        result = pi(max_iter);
    } else {
        result = pi_thread(max_iter, n_threads);
    }
    // FIXME: eu não faço ideia de como forçar o rust a retornar só o número de segundos. Essa coisa teima em formatar com um 's' no final! grr
    println!("{:?}", time.elapsed());
    if result == 10.0 {
        println!("the aggresive optimization destroys the benchmark so i'm using the result for something useless :p");
        // this print is outside the elapsed time so it will not affect the time but will force pi/pi_thread to be called
    }
}


fn pi(max_iterations: i32) -> f64 {
    let mut result: f64 = 0 as f64;

    for i in 0..max_iterations {
        result += 4.0 * (-1 as i32).pow(i as u32) as f64 * 1.0 / (2.0 * i as f64 +1.0);
        //FIXME jesus cristo que linha atroz. Revisar isso pra ficar legível
    }

    return result;
}

//TODO: considerar mudar a implementação pra usar Canais pra poder comparar mais diretamente com GO
// talvez canais (passagem de mensagem) seja uma abordagem inerentemente mais apropriada para problemas cpu-bound e compartilhamento de memória seja mais apropriada para problemas memory-bound
fn pi_thread(max_iterations: i32, n_threads: usize) -> f64 {
    let mut result: f64 = 0.0;
    let mut handles = Vec::new();//the type inference will deal with the type of this
    //let mut handles: Vec<thread::JoinHandle<_>> = Vec::new();
    //let mut handle: thread::JoinHandle<_>; <- this is the type signature of a handler!

    //spins up threads
    for i in 0..n_threads {
        // puts all handles in a vector
        // each thread spawn recieves a closure with the function
        // closures capture the current state, so they copy the current i into themselves (is expected behaviour? that happens, but should it?)
        // type annotation superfluous
        handles.push( thread::spawn(move || ->f64 {
            let mut r: f64 = 0.0;
            // TODO: im hoping it will capture i appropriatelly
            let start = i*max_iterations as usize/n_threads;
            let end = (i+1)*max_iterations as usize/n_threads;

            for j in start..end as usize {//computes pi partially
                r += 4.0 * (-1 as i32).pow(j as u32) as f64 * 1.0 / (2.0 * j as f64 +1.0);//FIXME jesus cristo que linha atroz. Revisar isso pra ficar legível
            }
            return r;
        }));
    }

    for handle in handles {
        // Wait for the thread to finish. Returns a result.
        result += handle.join().unwrap();
    }

    return result;
}
