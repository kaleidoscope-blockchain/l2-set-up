#!/usr/bin/bash

SEQUENCER_URL=https://sepolia-sequencer.base.org

sudo ./build/bin/geth \
  --ws \
  --ws.port=8546 \
  --ws.addr=0.0.0.0 \
  --ws.origins="*" \
  --ws.api=debug,eth,net,engine \
  --http \
  --http.port=8545 \
  --http.addr=0.0.0.0 \
  --http.vhosts="*" \
  --http.corsdomain="*" \
  --http.api=web3,debug,eth,net,engine \
  --authrpc.addr=localhost \
  --authrpc.jwtsecret=./jwt.txt \
  --authrpc.vhosts="*" \
  --datadir=./datadir \
  --verbosity=3 \
  --rollup.disabletxpoolgossip=true \
  --rollup.sequencerhttp=$SEQUENCER_URL \
  --rollup.halt=major \
  --nodiscover \
  --syncmode=full \
  --gcmode=archive \
  --maxpeers=100 \
  --op-network=base-sepolia
