# Changelog

# 0.3.14

* `badger_speakers_scheduled`: allow to mail speakers a second time
* `load_videos`: conform to the new sreview output format
* `load_videos`: overwrite videos

## 0.3.13

* Bug fixes to schedule timezone and volunteer permissions.

## 0.3.12

* Put auth on the volunteer views, so anonymous users get sent to log
  in, rather than 500ing.

## 0.3.11

* Volunteer tools:
  - Bug fixes for the volunteer timezone support.
  - Add a `required_permission` property to tasks.
  - Add a `task.accept_video_tasks` permission.

## 0.3.10

* Volunteer tools:
  - Allow importing video volunteer tasks from YAML, together with the
    ad-hoc tasks.
  - Display Volunteer views in the Volunteer's configured timezone.

## 0.3.9

* Tools for generating Jitsi, Etherpad, etc. URLs.

## 0.3.8

* schedule: improve navigation in single-day schedule pages.

## 0.3.7

* several improvements in the schedule:
  * drop track sidebar
  * improve display of local time
  * make video/no-video icon a bit smaller
  * add class to Time header cell to allow styling
  * add fullscreen mode

## 0.3.6

* generalize `badger_speakers_scheduled` to work for all future conferences.

## 0.3.5

* `load_schedule_grid`: schedule activities past midnight
* Add command to print a list of countries by talks, with notes

## 0.3.4

* Only look up the payment intent for new invoices
* bursary admin: list name and email

## 0.3.3

* Minor:
  * T-shirt instructions and help text.

## 0.3.2

* Minor:
  * Only mention expense bursaries, for online DebConfs, in confirmation
    emails, and the profile page.
  * Set registration completed timestamps.
  * Correctly determine registration completion in statistics, for
    online debconfs.
  * Render Kosovo, in country listings.
  * Include expense bursaries in admin views, statistics, exports.
  * Collect shipping addresses for online debconfs.

## 0.3.1

* Render invoices gracefully without Stripe credentials
* Add an event type breakdown to the content statistics

## 0.3.0

* Major changes:
  * Support DebConf Online (stripped down registration)
  * Replace PayPal payments with Stripe
* Bug fixes:
  * Avoid duplicating invoices when the total hasn't changed.

## 0.2.1

* Bug fixes:
  * Support anonymous views of the closed registration page
  * Drop unused imports
  * Drop use of six, we're py3k-only, baby
  * Fix volunteer statistics
  * Allow content statistics to render without a schedule
  * In Wafer > 0.7.7 slots have datetime fenceposts
  * Merge wafer.schedule templates from wafer 0.9.0
  * Django 2 compatibility: `is_authenticated` -> bool
  * Don't blow up if an event lost a venue
  * Fix volunteer admin
* Minor behavior changes:
  * Allow Content Admin to view users

## 0.2.0

* Port to Django 2:
  * Set `on_delete` on Foreign Keys
  * django.core.urlresolvers was renamed to django.urls in 1.10
  * Migration to update the bursaryreferee FK
* Port to wafer 0.9.0
  * debconf.views: fix against latest wafer >= 0.7.7
  * Update `load_schedule_grid` to support blocks
  * Make slot times TZ aware

## 0.1.22

* Move prices to a settings PRICES dict.

## 0.1.21

* Fix a bug in the bursary status, after DebConf has started.
* Add an invoice export.
* Add video player to talk pages.
* Simplify the volunteer task mapping data model.
* Mention the video team's advice for presenters, in the talk acceptance
  email.
* Add statistics pages for Volunteers and Content.
* Expose arrived and departed state to DCSchedule.
* Include Checked In state in bursary exports.
* Update the reimbursement email, to match current SPI requirements.

## 0.1.20

* UNKNOWN

## 0.1.19

* Support Conference Dinner in FD meal sales.
* Boldly show paid status in FD check-in.
* Set a deadline by which bursaries have to be approved, after which
  the user can be invoiced.
* Fail gracefully when a talk doesn't have a track (in the colouring
  code)
* Disable retroactive volunteering.

## 0.1.18

* More tweaks to video volunteer wrangling.

## 0.1.17

* Improve volunteer signup.
* Automate Video Team T-Shirt distribution.

## 0.1.16

* createtasks: load task template descriptions

## 0.1.15

* Add timestamps to Attendee's registration.
* Show if attendees registered late, in front desk.

## 0.1.14

* Allow volunteers to set their preferences.
* Return a 404 when a non-registered user tries to preview a badge.

## 0.1.13

* Support Postgres in the queue migration from 0.1.12

## 0.1.12

* Add a management command to create volunteer tasks from YAML
* Improve the track list in the schedule.
* Change registration permissions (only admins can take cash).
* Get badges working again.
* Assign keysigning IDs, and add a management command to sort them.

## 0.1.11

* Generalize the badger speaker script to all talk statuses.
* Add a keysigning export.

## 0.1.10

* Validate speaker attendance dates, when schedule editing.
* Use DebConf's custom schedule templates.
* Add Python 3.5 support to the load\_schedule\_grid command.

## 0.1.9

* Add a command to load schedule grid from YAML

## 0.1.8

* Add a badger for accepted talks
* Add travel\_from to the bursary export.

## 0.1.7

* List exports in front desk
* Add bursaries export

## 0.1.6

* Further improvements to the bursary notification email.

## 0.1.5

* Add management command to remind users to register.
* Include some details, useful for visas in the registration
  confirmation email.
* Handle unassigned rooms, correctly.
* Clear travel expense amount, when cancelling a travel bursary request.
* Add a CSV export for Child Care.
* Display meal lists, in order.
* Remove DC18 details from the bursary notification email.

## 0.1.4

* Correct the permission checked by bursary admin pages.

## 0.1.3

* Add a Volunteer Admin group.
* Add Kosovo to the list of countries.

## 0.1.2

* SECURITY: Don't show other registered attendees as room-mates, when
  nobody has rooms assigned.

## 0.1.1

* Package now has metadata and license.
* New management commands: `create_debconf_groups`,
  `load_tracks_and_talk_types`.

## 0.1.0

* Initial release, mostly ready for DebConf19.
