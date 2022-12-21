One file per currency pair (or other data).

One commit per snapshot in time.

Commit structure to navigate to times (skip-list or tree etc) in log time.

Perhaps instead of files having the data directly, make them have a hash (with a nonce).  That's not strictly speaking necessary, because we could hack up git to enforce the separation of knowledge.  But I'd rather be able to use off-the-shelf git tools as much as possible.
