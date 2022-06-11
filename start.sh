while true; do
    python "${PWD}/josee.py"
    echo
    echo "[$(date +%F) $(date +%T)] Oh, something went wrong, that's okay, I'll fix that in 3 seconds."
    echo
    sleep 3
done