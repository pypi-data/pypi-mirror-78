Changelog
=========
1.0.0 (released 2020-09-03)
---------------------------

- Dropped Python 2 compatibility
- Standards compliance: KnaveMiddleware now returns a 403 response for both
  unauthorized and unauthenticated conditions

0.3.2 (released 2018-06-11)
---------------------------

- Middleware now returns either a 401 or 403 error as appropriate, depending on
  whether a user has been authenticated.

0.3.1
-----

- Bugfix for issue where roles were incorrectly cached, causing checks
  for roles to fail where they should have passed

0.3
---

- Optimized role membership lookups
- Permission subclasses may now implement custom checking logic
- Added @ACL.role_provider and @role_decider decorators

0.2
---

- Initial release

