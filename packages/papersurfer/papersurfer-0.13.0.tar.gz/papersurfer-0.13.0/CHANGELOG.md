# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.13.0]
- fixed crash when opening details for "Theme issue: Stokes at 200"
- reload list after posting a new paper to list
- implement CI and capture test coverage
- add --debug argument
- improve interoperability with Mac/Windows
- save config, data and log files to system paths
- add --paths argument to print config file paths for easier cleanup
- fix and improve --dump-posts

## [0.12.0] - 2020-09-03
### Added
- cache data in a tinydb database to speed up start time and save on api calls

### Changed
- load all posts from mattermost
