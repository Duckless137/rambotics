#!/usr/bin/env bash

mkdir -p mnt backup # Make mount and backup dirs
sudo mount UUID=43CB-ABA7 mnt # Mount student processor

if [ $? -ne 0 ]; then
    echo "Mount failed :("
    exit $?
fi

echo "Making backups just in case..."
rsync -rp --delete mnt/ backup # Backup just in case
echo "Writing to device..."
sudo rsync -rp --delete --exclude=.* --exclude=mnt --exclude=backup . mnt # Flash device
echo "Done!"
sudo umount mnt # Unmount device
