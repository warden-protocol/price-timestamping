# Committing to a historic record for price data with git

We want to publicly commit to a historical record of price data.

We start by keeping track of the relevant price data in a git repository, and making git commits every so often, eg every hour (or every minute etc).

We regurlarly publish the new commit hash we get from git, eg `6241eeff1c779d53172dcef676aaae5245039fdd`, on relevant blockchains.

That hash commits us not only to the record state of the data, but also the entire history.

Here's how we reveal some information we committed to.  Let's assume we kept our data in a directory called `price_data`:

```
$ ls --all price_data/
.  ..  .git  data
$ tree price_data/
price_data/
`-- data
        `-- USD-GBP

2 directories, 3 files
```

(This step is just to show that `price_data` is a normal git repository.)

Cargo/Rust installation

```
curl https://sh.rustup.rs -sSf | sh

```

additional dependencies for ubuntu

```
sudo apt install libssl-dev
sudo apt install pkg-config

```

We want to reveal the exchange rate for USD-GPB as of 24 hours ago.

So let's produce the proof with the following syntax:

```
$ cd root-path-containing-repository/

$ cargo run  --manifest-path <path-to-manifest/Cargo.toml> <path-to-repo/> <proof_output/> <some-commit-hash> <integer-number-commits> <path-to-pricefile/USD-GBP>
```
For our exemplary repo:

```
$ cd root-path-containing-repository/

$ cargo run  --manifest-path qredo-analytics/git-merkle-ing/Cargo.toml qredo-analytics/ proof_output/ fab308fce5f648b52be0f93a3a3848f79cc4db14 1 git-merkle-ing/price_data/data/USD-GBP
```

The proof is now in `proof_output`.  It happens to be a git repository, too.  A repository that only has exactly what we need to reveal the relevant information, and nothing more.

Here is how you can consume and verify the proof with *off-the-shelf standard git*:

```
$ cd proof_output/
$ git show 6241eeff1c779d53172dcef676aaae5245039fdd~24:data/binance/USD-GBP
exchange rate for USD-GBP at 2022-12-14 08:15:09.989070+00:00 is 2.8584
```

The same hash works for multiple timestamps and currency pairs.  Eg for 11 hours in the past of USD-SGD:
```
$ git-merkle-ing price_data/ proof_output_2/ 6241eeff1c779d53172dcef676aaae5245039fdd 11 data/binance/USD-SGD
content: exchange rate for USD-SGD at 2022-12-14 21:15:09.989070+00:00 is 0.35782
```

And verification:
```
$ cd proof_output_2/
$ git show 6241eeff1c779d53172dcef676aaae5245039fdd~11:data/binance/USD-SGD
exchange rate for USD-GBP at 2022-12-14 21:15:09.989070+00:00 is 1.45
```

For illustration of having just the relevant data only: the proof we just produced only has data to verify the price 11 hours ago.  If we try to use it to verify another price, we get an error:

```
$ cd proof_output_2/
$ git show 6241eeff1c779d53172dcef676aaae5245039fdd~24:data/binance/USD-GBP
error: Could not read 42a0ec5eeb6433f0bfd35cacf80e1610cdc81c60
error: Could not read 42a0ec5eeb6433f0bfd35cacf80e1610cdc81c60
fatal: invalid object name '6241eeff1c779d53172dcef676aaae5245039fdd~24'.
```

# Example from the kernel

Here's an example using the Linux kernel, to show that we can also handle huge repositories:

```
$ git-merkle-ing linux-kernel/ /tmp/proof 041fae9c105ae342a4245cf1e0dc56a23fbb9d3c 23 Documentation/gpu/backlight.rst
content: =================
Backlight support
=================

.. kernel-doc:: drivers/video/backlight/backlight.c
   :doc: overview

.. kernel-doc:: include/linux/backlight.h
   :internal:

.. kernel-doc:: drivers/video/backlight/backlight.c
   :export:
```

```
$ gtar c /tmp/proof/ | xz | wc -c
57232
```
And verification:

```
$ cd /tmp/proof/
$ git show 041fae9c105ae342a4245cf1e0dc56a23fbb9d3c~23:Documentation/gpu/backlight.rst
=================
Backlight support
=================

.. kernel-doc:: drivers/video/backlight/backlight.c
   :doc: overview

.. kernel-doc:: include/linux/backlight.h
   :internal:

.. kernel-doc:: drivers/video/backlight/backlight.c
   :export:
```

# Running the services in this repo

This is a work in progress.

Amongst other things, you need:
- `.env` and `priceapi/fastapi/app/.cfg` config files.
- you need to start `running1.bash` (and leave it running) and then start `running2.bash`

THere might be more steps necessarily.  We will document them as we clean things up.
