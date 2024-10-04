#!/bin/sh

cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/cod.py $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/cod.py
chmod +x $BASE_DIR/target/etc/init.d/S41network-config
$BASE_DIR/labsisop-buildroot/output/host/usr/bin/i686-buildroot-linux-uclibc-gcc custom-scripts/syscall_test.c -o $BASE_DIR/output/target/usr/bin/syscall_test
