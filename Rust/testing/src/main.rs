//use std::thread;//spawning threads
use crossbeam_utils::thread;//for scoped threads that borrow variables in the stack

fn main() {
    let m1 = vec![vec![1; 6];6];
    let m2 = vec![vec![2; 6];6];
    let mut res = vec![vec![0; 6];6];

    println!("what");
    print_matrix(&m1);
    println!("");
    print_matrix(&m2);

    //let mut handles = vec![];
    let n_threads = 4;
    let n_chunks = n_threads; //chopping up result in equal parts
    let res_len = res.len();

    // update: apparently the iteration goes over the remainder too!
    // chunks returns an iterator for sucessfully created chunks and a a remainder, which didn't fit into a chunk!
    // if size % n_threads != 0 it might cause trouble (part of the matrix will be untouched)
    let chunks = res.chunks_mut(res_len / n_chunks as usize);

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
                println!("from thread: {}", m1[0][0]);
                println!("from thread: {}", chunk[0][0]);
            }));
        }

        //crossbeam guarantees join at the end
        /*for handle in handles {
            handle.join();
        }*/
    }).unwrap();

    println!("result:");
    print_matrix(&res);
}


fn print_matrix(m : &Vec<Vec<i32>>){
    for row in m{
        for col in row {
            print!("{} ", col);
        }
        println!();
    }
}

//pressupõe matrix quadrada
fn matrix_mult(m1 : &Vec<Vec<i32>>, m2 : &Vec<Vec<i32>>, result : &mut Vec<Vec<i32>>){

    for i in 0..result.len() { //for each line i in the result matrix/slice
        for j in 0..result[i].len() { //for each position j in these lines
            for k in 0..result.len() { //iterate through respective m1 row and m2 column
                result[i][j] += m1[i][k] * m2[k][i]; // operate, add, accumulate result in result[i][j]
            }
        }
    }

    return;
}
