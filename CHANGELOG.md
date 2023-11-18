# Changelog
All notable changes to this project will be documented in this file.

## 0.2.0 - 18 November 2023
### Added
- Default tab support
- Notebook tab support
- Print debug info for Blacklist
- New setting `context_delimiter`: Allows you to specify expected history format for Notebook and Default tabs, defaults to `\n`

### Changed
- Renamed `Message Delimiter` to `Negative Delimiter`
- Blank history messages are now ignored

## 0.1.0 - 16 November 2023
### Added
- New Blacklist feature: Allows you to exclude certain terms from being injected into your negative prompt, with support for * wildcard and regex
- `CHANGELOG.md` to track changes

### Changed
- Increased default `history_multiplier` from 0 to 1 (I'm still experimenting with different defaults; your feedback is appreciated)

## 0.0.2 - 15 November 2023
### Fixed
- Fixed missing key for `enable` parameter
- Fixed `history_length` datatype issue
- Corrected typos in README

## 0.0.1 - 15 November 2023
### Added
- Initial release