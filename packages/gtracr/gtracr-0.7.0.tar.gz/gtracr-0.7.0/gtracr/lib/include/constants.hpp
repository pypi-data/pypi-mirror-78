// contains relavant constants used within the package

#ifndef __CONSTANTS_HPP_
#define __CONSTANTS_HPP_

namespace constants {
constexpr double SPEED_OF_LIGHT = 299792458.;
constexpr double ELEMENTARY_CHARGE = 1.602e-19;
constexpr double RE = 6371.2 * (1e3);
constexpr double pi = 3.14159265;
constexpr double DEG_TO_RAD = pi / (180.);
constexpr double RAD_TO_DEG = 180. / pi;
constexpr double KG_PER_GEVC2 =
    1.78e-27;  // conversion factor between kg and GeV/c^2
constexpr double KG_M_S_PER_GEVC =
    5.36e-19;  // conversion factor between kg m/s (momentum SI units) and GeV/c
}  // namespace constants

#endif  //__CONSTANTS_HPP_