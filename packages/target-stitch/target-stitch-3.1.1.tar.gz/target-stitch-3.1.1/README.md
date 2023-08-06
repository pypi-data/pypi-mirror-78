# target-stitch

Reads [Singer](https://singer.io) formatted data from stdin and persists it to the Stitch Import API.

## Install

Requires Python 3.5.6

```bash
› pip install target-stitch
```

## Use

target-stitch takes two types of input:

1. A config file containing your Stitch client id and access token
2. A stream of Singer-formatted data on stdin

Create config file to contain your Stitch client id and token:

```json
{
  "client_id" : 1234,
  "token" : "asdkjqbawsdciobasdpkjnqweobdclakjsdbcakbdsac",
  "small_batch_url": "https://api.stitchdata.com/v2/import/batch",
  "big_batch_url": "https://api.stitchdata.com/v2/import/batch",
  "batch_size_preferences": {}
}
```
```bash
› tap-some-api | target-stitch --config config.json
```

where `tap-some-api` is [Singer Tap](https://singer.io).

---

Copyright &copy; 2017 Stitch
