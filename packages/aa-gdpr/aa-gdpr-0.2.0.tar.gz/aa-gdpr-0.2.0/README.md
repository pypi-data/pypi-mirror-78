# AA-GDPR

A Collection of overrides and resources to help Alliance Auth installs meet GDPR legislation.

This Repository cannot guarantee your Legal requirements but aims to reduce the technical burden on Web/System Administrators

## Current Features

Overrides Alliance Auth default resource bundles to use staticfile delivery.

Local staticfile delivery of  resources to avoid using CDNs

* Javascript
  * Less 3.12.2
  * Moment.js 2.27 <https://github.com/moment/moment>
  * jQuery 3.5.1 & 2.2.4 <https://github.com/jquery/jquery>
  * jQuery-DateTimePicker 2.5.20 <https://github.com/xdan/datetimepicker>
  * Twitter-Bootstrap 3.4.1 <https://github.com/twbs/bootstrap>
  * x-editable 1.5.1 <http://vitalets.github.io/x-editable>
  * Less 2.7.3 & 3.12.2 <http://lesscss.org/>
  * DataTables 1.10.21 <http://datatables.net/>
  * Clipboard.js 2.0.6 <https://clipboardjs.com/>
* Fonts
  * FontAwesome 5.14 <https://github.com/FortAwesome/Font-Awesome>
  * OFL Lato 16 <https://fonts.google.com/specimen/Lato>
* CSS
  * DataTables 1.10.21 <http://datatables.net/>
  * FontAwesome 5.14 <https://github.com/FortAwesome/Font-Awesome>
  * jQuery-DateTimePicker 2.5.20 <https://github.com/xdan/datetimepicker>
  * x-editable 1.5.1 <http://vitalets.github.io/x-editable>

## Planned Features

* Consent Management
* Terms of Use Management
* Data Transparency
* Right to be Forgotten Requests

## Installation

### Step One - Install

Install the app with your venv active

```bash
pip install aa-gdpr
```

### Step Two - Configure

* Add `INSTALLED_APPS.insert(0, 'aagdpr')` right before your `INSTALLED_APPS` list in your projects `local.py`
* Add the below lines to your `local.py` settings file

 ```python
## Settings for AA-GDPR ##

# Instruct third party apps to avoid CDNs
 AVOID_CDN = False
```

### Step Three - Update Project

* Run migrations `python manage.py migrate` (There should be none yet)
* Gather your staticfiles `python manage.py collectstatic`

## Settings

AVOID_CDN - Will attempt to instruct third party applications to attempt to load CSS JS and Fonts from staticfiles, Default `False`.