# Changelog

## 1.1.1 (2020-08-26)
### Improvements
- Added default lookup paths for OpenCV on Ubuntu 20.04, enabling building from source out of the box there. 
- Added parameter to specify the focal length of the camera supplying the eye images for a more accurate 3D model.

## 1.1.0 (2020-05-04)
### Changed
- Changed the default 2D detector properties to be the same as the default overrides that the 3D detector applies.

## 1.0.5 (2020-04-20)
### Added
- Added option to run 3D detector without internal 2D detector, but from serialized data of external 2D detector

## 1.0.4 (2020-01-13)
### Fixed
- Fixed crash when installing from source distribution package

## 1.0.3 (2020-01-07)
### Fixed
- Wrong Roi.rect() computation.

## 1.0.2 (2019-12-03)
- Initial release.