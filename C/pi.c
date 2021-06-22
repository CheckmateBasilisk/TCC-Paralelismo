#include<stdio.h>
#include <time.h>
#include<math.h>


double pi(int maxIter){
    double result = 0;

    for (int i = 0; i < maxIter; i++) {
        result += 4.0 * pow(-1, i * 1) / (i*2+1);//geez, to type coersion then? not ever some kind of numeric supertype?
    }

    return result;
}


int main(){
    int maxIter = 1000000000;
    clock_t start, end;
    double cpu_time_used;


    start = clock();
    printf("hellothere");
    printf("%lf\n", pi(maxIter));
    end = clock();

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("%lf\n", cpu_time_used);

    return 0;
}
