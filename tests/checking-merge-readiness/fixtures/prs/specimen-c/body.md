Introduces a tag-based cache invalidation framework. Handlers register
the cache tags their responses depend on; writers publish invalidation
events to the invalidation bus, and the cache middleware drops every
cached entry carrying an affected tag. The products endpoint is migrated
as the first consumer. The registry supports cross-service invalidation
so other services can subscribe to tag events later.

Includes an admin endpoint `POST /admin/cache/flush` for flushing entries
by tag during incidents.
