# lightbringer

Very simple NSQ client library. Exposes a very small API to publish and read from a NSQ cluster.

Supports only (but supports them well, with a complete test suite covering all the code)
- TCP connections to nsqd (no HTTP connections)
- nsqlookupd setups
- publish only to a single server
- keepalives (TOUCH) of inflight messages
- messages are requeued at connection close

Not supported:
- tls connections
- snappy/deflate connections


### Examples

#### Write

```python
mesage = b'some data'
async with lightbringer.Writer('127.0.0.1:4150', topic='topic') as writer:
	await writer.pub(message)
	await writer.dpub(message, delay)
```

#### Read from `nsqd` servers
```python
async with lightbringer.Reader(
	nsqd_tcp_addresses=['127.0.0.1:4150'],
	lookupd_http_addresses=['http://127.0.0.1:4161'], # will poll this regularly and merge with the list of direct connections
	topic='topic',
	channel='channel#ephemeral',
	max_in_flight=10, # applied per connection, so if the lookups map to 30 nsqd and the tcp_addresses lists 20 other addresses, there might be up to 500 in flight messages here
) as reader:
	async for msg in reader:
		print(msg, msg.nsqd_host, msg.body)
		await msg.touch()
		await msg.fin()
		await msg.req()
		await msg.req(timeout=10)
```


#### Read from `nsqd` servers - only accept messages one at a time
```python
async with lightbringer.SingleMessageReader(
	lookupd_http_addresses=['http://127.0.0.1:4161'],
	topic='topic',
	channel='topic',
) as reader:
	async for msg in reader:
		await msg.fin()
```
