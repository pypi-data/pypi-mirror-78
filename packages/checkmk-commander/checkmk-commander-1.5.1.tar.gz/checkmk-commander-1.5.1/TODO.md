TODO
----

See also gitlab issues.

* Warn on install if path is not in PATH
* Move all requests.get to a function and add timeout, user agent, etc
* See if WATO funcitons should be split to a library.

* Make a path from allhosts -> details -> services on that host
* Improve readability, colors.
* Find down time for down-alerts.
* Fetch host comments for down hosts.
* Status bar at bottom could be replaced by a scrolling textview with "Host- and Service events"?
* Icon, desktop integration.
* I can only assume syslog is os dependent.
* Write more unit tests
* Change URLs to be an object, for testing and safer handling.


High pri features
-----------------

* [x] list service problems from several checkmk instances
* [x] ack service problems
  * [x] Show popup to add comment
  * [x] Parse time from comment
  * [x] ack service problems on all sites, not just main host
* [x] ack host problems
* [x] downtime service problems
* [x] comment service problems
* [x] show down hosts

Medium pri features
----------------

* [x] Reinventorize a host
* [x] Make actions async
* [x] Add logging
* [x] show service problem count

Low pri features
----------------

* [x] Ability to run remotely (without being on checkmk host)
* [x] Reschedule check
* [ ] Add new host
* [ ] Search in alert list
* [ ] Search in all host/services (to i.e. run a reinventorize before anything complains)
* [ ] Sort alert list
* [ ] Show number of comments on services in overview
* [x] List event notifications
* [ ] List hosts/services in downtime
* [ ] More list options, like remove numbering, wrap/clip columns.
