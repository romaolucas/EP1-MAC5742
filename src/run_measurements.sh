#! /bin/bash

set -o xtrace

MEASUREMENTS=10
ITERATIONS=10
INITIAL_SIZE=16
INITIAL_NTHREADS=1

SIZE=$INITIAL_SIZE

NTHREADS=$INITIAL_NTHREADS

NAMES=('mandelbrot_seq' 'mandelbrot_pth' 'mandelbrot_omp')

make
mkdir results

for NAME in ${NAMES[@]}; do
    mkdir results/$NAME
    if [ "$NAME" == "mandelbrot_seq" ] ; then 
        for ((i=1; i<=$ITERATIONS; i++)); do
                perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE >> full.log 2>&1
                perf stat -r $MEASUREMENTS ./$NAME -0.8 -0.7 0.05 0.15 $SIZE >> seahorse.log 2>&1
                perf stat -r $MEASUREMENTS ./$NAME 0.175 0.375 -0.1 0.1 $SIZE >> elephant.log 2>&1
                perf stat -r $MEASUREMENTS ./$NAME -0.188 -0.012 0.554 0.754 $SIZE >> triple_spiral.log 2>&1
                SIZE=$(($SIZE * 2))
        done
    elif [ "$NAME" == "mandelbrot_omp" ]; then
        while [ $NTHREADS -le 32 ]; do
            export OMP_NUM_THREADS=$NTHREADS
            for ((i=1; i<=$ITERATIONS; i++)); do
                    perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE >> full_$NTHREADS.log 2>&1
                    perf stat -r $MEASUREMENTS ./$NAME -0.8 -0.7 0.05 0.15 $SIZE >> seahorse_$NTHREADS.log 2>&1
                    perf stat -r $MEASUREMENTS ./$NAME 0.175 0.375 -0.1 0.1 $SIZE >> elephant_$NTHREADS.log 2>&1
                    perf stat -r $MEASUREMENTS ./$NAME -0.188 -0.012 0.554 0.754 $SIZE >> triple_spiral_$NTHREADS.log 2>&1
                    SIZE=$(($SIZE * 2))
            done
            NTHREADS=$(($NTHREADS * 2))
            SIZE=$INITIAL_SIZE
        done
    fi
    SIZE=$INITIAL_SIZE

    mv *.log results/$NAME
    rm output.ppm
done
