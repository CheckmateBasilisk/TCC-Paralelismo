use std::time::Instant;
use std::env;
use crossbeam_utils::thread;//for scoped threads that borrow variables in the stack :D
use rand::Rng;

fn main() {
    let n = 1000;//mds do céu Rust corre mto...
    let args: Vec<String> = env::args().collect();//geting args from cmd line
    let n_threads:usize = args[1].parse::<i32>().unwrap() as usize;//converting arg['nthreads'] to uint

    //dynamically creates nxn matrix
    //creates m1 m2 and result as vectors; which are arrays without defined size at compile time
    let m1: Vec<Vec<i32>> = random_matrix(n,-10,10);
    let m2: Vec<Vec<i32>> = random_matrix(n,-10,10);
    let mut result = vec![vec![0i32; n]; n];

    let time = Instant::now();
    if n_threads == 0 {
        // TODO: será q vou ter que sacanear o compilador dnv pra não otimizar isso aqui dms?
        matrix(&m1, &m2, &mut result);
    } else {
        matrix_thread(&m1, &m2, &mut result, n_threads);
    }
    println!("{:?}", time.elapsed());

}

// given m1, m2, computes m1 x m2 and stores the result in the parameter result
// supposes m1 and m2 are nxn
// will not deal with misuse
fn matrix(m1: &Vec<Vec<i32>>, m2: &Vec<Vec<i32>>, result: &mut Vec<Vec<i32>>) {
    for i in 0..result.len() {
        for j in 0..result[i].len() {
            for k in 0..m1[i].len() {
                result[i][j] += m1[i][k] * m2[k][j];
            }
        }
    }
}

// given m1, m2, computes m1 x m2 and stores the result in the parameter result
// supposes m1 and m2 are nxn
// will not deal with misuse
// splits the workload in disjoint chunks and uses scoped threads to tell rust the threads are joined before the current scope ends
fn matrix_thread(m1: &Vec<Vec<i32>>, m2: &Vec<Vec<i32>>, result: &mut Vec<Vec<i32>>, n_threads: usize){
    //chopping up result in equal parts
    let n_chunks = n_threads;
    let res_len = result.len();
    let chunks = result.chunks_mut(res_len / n_chunks as usize);
    // update: apparently the iteration goes over the remainder too!
    // chunks returns an iterator for sucessfully created chunks and a a remainder, which didn't fit into a chunk!
    // if size % n_threads != 0 it might cause trouble (part of the matrix will be untouched)

    thread::scope(|s| {
        let mut handles = vec![];
        for chunk in chunks {
            // these variables will be moved into the threads and lost to the current scope, which is ok!
            // otherwise the only available variables m1 and m2 would have been moved to the first thread, starving the others of variables/references to the data
            // They are references to the original matrices
            let m1 = &m1;
            let m2 = &m2;
            // let mut chunk = chunk.to_vec(); //this breaks. at some point it makes a copy and doesnt update the original. Is it to_vec() ?

            handles.push(s.spawn(move |_| {
                //println!("A child thread borrowing `chunk`: {:?}", chunk);
                //matrix_mult(&m1, &m2, &mut chunk.to_vec());


                for i in 0..chunk.len() { //for each line i in the result matrix/slice
                    for j in 0..chunk[i].len() { //for each position j in these lines
                        for k in 0..chunk[i].len() { //iterate through respective m1 row and m2 column
                            chunk[i][j] += m1[i][k] * m2[k][i];
                        }
                    }
                }
            }));
        }

        //crossbeam guarantees join at the end
        // i'm also ignoring any errors that might occur
        /*for handle in handles {
            handle.join();
        }*/
    }).unwrap();
}

//FIXME: tem algo errado com a geração de matrix aleatória. Ele gera um único valor e copia um monte d vezes
// acho q fica fácil se eu usar um map
fn random_matrix(n: usize, min: i32, max: i32) -> Vec<Vec<i32>> {
    let mut rng = rand::thread_rng();//apparently this innitializes the rng engine
    let result = vec![vec![rng.gen_range(min..max); n]; n];

    return result;
}
