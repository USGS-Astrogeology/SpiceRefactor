#ifndef ALE_ORIENTATIONS_H
#define ALE_ORIENTATIONS_H

#include <vector>

#include "Rotation.h"

namespace ale {
  class Orientations {
  public:
    /**
     * Construct a default empty orientation object
     */
    Orientations() {};
    /**
     * Construct an orientation object give a set of rotations
     * and optionally angular velocities at specific times.
     */
    Orientations(
      const std::vector<Rotation> &rotations,
      const std::vector<double> &times,
      int source,
      int destination,
      const std::vector<std::vector<double>> &avs = std::vector<std::vector<double>>()
    );
    /**
     * Orientations destructor
     */
    ~Orientations() {};

    std::vector<Rotation> rotations() const;
    std::vector<std::vector<double>> angularVelocities() const;
    std::vector<double> times() const;
    int source() const;
    int destination() const;

    /**
     * Get the interpolated rotation at a specific time.
     */
    Rotation interpolate(
      double time,
      RotationInterpolation interpType=SLERP
    ) const;
    /**
     * Get the interpolated angular velocity at a specific time
     */
    std::vector<double> interpolateAV(double time) const;
    /**
     * Rotate a position or state vector at a specific time
     */
    std::vector<double> rotateAt(
      double time,
      const std::vector<double> &vector,
      RotationInterpolation interpType=SLERP,
      bool invert=false
    ) const;

  private:
    std::vector<Rotation> m_rotations;
    std::vector<std::vector<double>> m_avs;
    std::vector<double> m_times;
    int m_source;
    int m_destination;
  };
}

#endif
