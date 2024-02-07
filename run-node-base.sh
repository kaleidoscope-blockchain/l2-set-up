#!/usr/bin/bash

sudo bin/op-node \
  --l1=<L1_RPC_URL> \
  --l2=ws://localhost:8551 \
  --rpc.addr=0.0.0.0 \
  --rpc.port=9545 \
  --l2.jwt-secret=./jwt.txt \
  --network=base-sepolia \
  --rollup.halt=major \
  --rollup.load-protocol-versions=true
