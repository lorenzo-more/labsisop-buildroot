#!/bin/sh

cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/cod.py $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/cod.py
chmod +x $BASE_DIR/target/etc/init.d/S41network-config

