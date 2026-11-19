function deepchecksum --description="Uses hashdeep tools to create checksums of the current directory"
    set DATE (date +%F_%A)
    set BASEDIR (basename $PWD)
    set BASEDIR (string replace -a ' ' _ "$BASEDIR")
    set HASH_FUNCTIONS md5deep sha1deep sha256deep tigerdeep whirlpooldeep
    set SIG_DIR Signatures_for_{$BASEDIR}

    mkdir -p $SIG_DIR

    for HASH in $HASH_FUNCTIONS
        "$HASH" -rl . > "$SIG_DIR"/"$BASEDIR"_"$HASH"_"$DATE"
    end

end


