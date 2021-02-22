export MAX_DOWNLOAD_SPEED=0
export MAX_CONCURRENT_DOWNLOADS=16
aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800 --check-certificate=false \
   --max-connection-per-server=10 --rpc-max-request-size=1024M \
   --seed-time=0.01 --seed-ratio=1.0 --min-split-size=10M --follow-torrent=mem --split=10 \
   --daemon=true --allow-overwrite=true --max-overall-download-limit=$MAX_DOWNLOAD_SPEED \
   --max-overall-download-limit=0 --max-overall-upload-limit=0 --max-concurrent-downloads=$MAX_CONCURRENT_DOWNLOADS