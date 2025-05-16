#!/bin/bash

> tiempos_clientes.log

iteraciones=(25 100 200 700 1500 3000)
max_nodos=7

for num in "${iteraciones[@]}"; do
    for ((i=1; i<=$max_nodos; i++)); do
    echo "TEST Nodos: $i, Iteraciones: $num"
        ./montaje.sh $i $num
    done
done
