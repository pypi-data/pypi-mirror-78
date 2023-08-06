Knave: ACLs and authorization in WSGI apps
===========================================

Knave provides roles/groups and permissions based authorization
for web (WSGI) applications.
Knave assigns roles to users
(both site wide roles like 'administrator' and
context-sensitive roles like 'creator'),
then uses those roles to decide whether the user has permission to carry out an
action.

You can configure permissions and roles statically in your code, or
write adapters to pull authorization information from a database or other
backend.

Knave doesn't do authentication, but can hook into most authentication systems.

`Knave Authorization Documentation <https://ollycope.com/software/knave/latest/>`_
\| `Repository <https://hg.srt.ht/~olly/knave/>`_



