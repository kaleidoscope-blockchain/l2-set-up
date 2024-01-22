#!/usr/bin/bash

SEQUENCER_URL=https://goerli-sequencer.optimism.io/


sudo ./build/bin/geth \
  --ws \
  --ws.port=8546 \
  --ws.addr=0.0.0.0 \
  --ws.origins="*" \
  --http \
  --http.port=8545 \
  --http.addr=0.0.0.0 \
  --http.vhosts="*" \
  --http.corsdomain="*" \
  --http.api=web3,debug,eth,net,engine \
  --authrpc.addr=localhost \
  --authrpc.jwtsecret=./jwt.txt \
  --authrpc.port=8551 \
  --authrpc.vhosts="*" \
  --datadir=./datadir \
  --verbosity=3 \
  --rollup.disabletxpoolgossip=true \
  --rollup.sequencerhttp=$SEQUENCER_URL \
  --nodiscover \
  --syncmode=full \
  --gcmode archive \
  --maxpeers=0 \
  --rollup.halt=major \
  --op-network=op-goerli
