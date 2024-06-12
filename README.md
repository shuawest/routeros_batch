# Ansible Collection - shuawest.routeros_batch

Modules for MikroTik RouterOS idempotent script generation, script execution, and batch fact retrieval

NOTE: This collection is not supported - use at your own risk


## Included content

- `shuawest.routeros_batch.script` - Add, remove, execute a named script on a Mikrotik RouterOS device
- `shuawest.routeros_batch.facts` - Fetch facts with a list of paths using the Mikrotik RouterOS api
- `shuawest.routeros_batch.scriptgen` - Generate Mikrotik RouterOS script to modify configuration with idempotent configuration


## Using this collection

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for general detail on using collections.

This module connects with the HTTP/HTTPS API over the `community.routeros.api` and `api_facts` modules.


### Edge cases

Please note that `routeros_batch.script` uses the `community.routeros.api` module, which does **not** support Windows jump hosts.
