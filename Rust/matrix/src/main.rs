use std::time::Instant;
use rand::Rng;

fn main() {
    let n = 4*300;//mds do céu Rust corre mto...
    //dynamically creates nxn matrix
    //creates m1 m2 and result as vectors; which are arrays without defined size at compile time
    let m1 = random_matrix(n,-10,10);
    let m2 = random_matrix(n,-10,10);
    let mut result = vec![vec![0i32; n]; n];

    let time = Instant::now();
    matrix(&m1,&m2,&mut result);
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

fn random_matrix(n: usize, min: i32, max: i32) -> Vec<Vec<i32>> {
    let mut rng = rand::thread_rng();//apparently this innitializes the rng engine
    let result = vec![vec![rng.gen_range(min..max); n]; n];

    return result;
}
