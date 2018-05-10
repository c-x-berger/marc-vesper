Standard Protocol
===

This document roughly outlines the MARC Vesper protocol as it should be implemented.

Terms with specific definitions are in _italics_ (e.g. _client_). Definitions are located at the end of this document.
Emphasis is indicated with **bold text** at author's discretion.
All strings, when encoded to/decoded from binary (for signing, transmission, etc) are handled as UTF-8.

## Typecodes

Most operations are performed by sending lists of the form `[primarydata, extradata, type]` to other machines. The last item, `type`, is an integer representing what the recipient should do with the recieved data. These numbers follow a simple scheme.

The first digit represents what kind of request the data is.

Request type | Codes
--- | ---
Change resource | 1XX
Get resource | 2XX

The second digit represents the source of the request.

Request source | Codes
--- | ---
Client | X0X
Server | X1X

The third and final digit is unique to each operation. There may be many operations for a server to get data from another server (the `21X` range), but only one for getting a specific value.

## Updating a resource
Type of operation | Typecode
--- | ---
Client edits server | 100
### In general
Updating a _resource_ involves two machines: a _client_ and a _server_. In order to update a _resource_, the _client_ must:
1. Choose a _resource_ to update (typically by name/label)
2. Provide the **verifying** key that was originally used to claim the _resource_ (currently, key changes are not supported except by manual editing)
3. Prove control over the signing key by signing the update as sent to the _server_

This data is then sent to the _server_, which is responsible for checking the _client's_ signature and updating its stored data to match.
### In specifics
The _client_ creates a list of two items: the update to perform and the signature of that update.
The update is represented as a JSON dictionary with the following key/value pairs:
* `label`: A string indicating the _resource_ to update
* `value`: A string (or other data encodable with UTF-8) indicating the new value for the _resource_.
* `serial_no`: The current UNIX time. (Obtained with `datetime.datetime.now(datetime.timezone.utc).timestamp()` in Python)
* `key`: The verify key to use for this update. It is a NaCL verifying key encoded as URL-safe base 64.

The second list item is the signature of the above data as a JSON object. The list is then encoded as JSON for a final result that looks similar to the following example (indentation and linebreaks optionally included for readability):

```json
[
    {
        "label": "lol.hype",
        "serial_no": 1520624236.476263,
        "key": "gcx-__2s4l_5bHHepX2vOF-nNBr_FZ2KHuT1O6EMR0w=",
        "value": "lol.lol.lol.lol"
    },
    "nR-ZN3SeMFeavl0l2ceBEuJLqPSPsV2RuSEthzAxz6VSqOr1BDk95751OKebhsDImVOtx85UC4lfsH0OkGFuCXsibGFiZWwiOiAibG9sLmh5cGUiLCAic2VyaWFsX25vIjogMTUyMDYyNDIzNi40NzYyNjMsICJrZXkiOiAiZ2N4LV9fMnM0bF81YkhIZXBYMnZPRi1uTkJyX0ZaMktIdVQxTzZFTVIwdz0iLCAidmFsdWUiOiAibG9sLmxvbC5sb2wubG9sIn0=",
    100
]
```

This JSON is then sent to the _server_ for handling. After verifying the signature against both the given key (to yet futher ensure integrity of the data) and the stored key (if any).
If both signatures are valid, the _server_ silently updates its stored data. If either signature is invalid, the server silently discards the update.
Signatures may be considered invalid if the serial number is:
* In the future by more than a given limit chosen by the _server_
* In the past by more than a given limit chosen by the _server_

In niether case is the _client_ given any explicit response. 

## Getting a resource
Type of operation | Typecode
--- | ---
Client queries server | 200
### In general
The _client_ sends a small request to the _server_ for the _resource_ at a specific label. The _server_ responds with what data it has, or a _resource_ with all fields set as `""` (i.e. empty string) if it has none.
### In specifics
The _client_ sends a UTF-8 encoded JSON list to the _server_ in the following form:
```json
[
    "foo.bar",
    "",
    200
]
```
The second item in the list is arbitrary - for a 200 request it has no special meaning and it may be entirely disregarded by the _server._ It is kept in the list at all to satisfy the standard request format (i.e. `[primarydata, extradata, type]`.)

The _server_ then responds to the _client_ with a UTF-8 encoded JSON dictionary containing the known information about the _resource._ This dictionary is structured as follows:
```json
{
    "foo.bar": {
        "value": "baz",
        "key": "ObVIOUSlyTHisISAnExamPLEKEy"
    }
}
```
If the _server_ has data about the _resource_ beyond label, value, and key, it **may** choose to add those values as well. They should be included as key/value pairs in the dictionary (in this case, the `"foo.bar"` dictionary.)

## Definitions

* Resource: A piece of information stored by the server, edited by the first _client_ to claim it. All resources contain the following:
  * A label that identifies the resource uniquely from other resources
  * A value to be stored
  * A verifying key to use when checking updates to the resource
  
  Optionally, a resource may contain other data (such as human-readable owner names, last update time, and type of resource.)
* Client: A computer which connects to a _server_ an makes various kinds of requests (update, get, etc). Not required to store information about any resource or be able to produce information about any _resource_, except when it wishes to change that _resource_.
* Server: A computer which handles requests from _clients_ as well as other _servers_ for information requests, updates, etc. Required to store or be otherwise able to produce the following data for any claimed _resource_:
  * The value of that resource
  * The key used for verifying updates to that resource
