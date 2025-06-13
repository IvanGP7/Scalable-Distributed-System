#!/bin/bash

> tiempos_clientes.log
> worker.log

iteraciones=(25 200 700 1500 3000 7000 12000 20000 50000 100000)
max_nodos=(1 4 7 10)

for num in "${iteraciones[@]}"; do
    for i in "${max_nodos[@]}"; do
    echo "TEST Nodos: $i, Iteraciones: $num"
        ./montaje.sh $i $num
        sleep 2
    done
done
