#!/bin/sh

# copy files from host to target
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/cod.py $BASE_DIR/target/usr/bin

# changing permissions
chmod +x $BASE_DIR/target/usr/bin/cod.py
chmod +x $BASE_DIR/target/etc/init.d/S41network-config

# compiling c code
$BASE_DIR/host/usr/bin/i686-buildroot-linux-uclibc-gcc custom-scripts/syscall_test.c -o $BASE_DIR/target/usr/bin/syscall_test
