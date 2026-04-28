"""Shared control helpers for the two-wheel drive stack."""


def clamp(value: float, lower: float = -1.0, upper: float = 1.0) -> float:
    """Clamp a scalar value between the provided bounds."""
    return max(lower, min(value, upper))


def clamp_twist(
    linear_x: float,
    angular_z: float,
    limit: float = 1.0,
) -> tuple[float, float]:
    """Clamp linear and angular velocity components to a symmetric limit."""
    return clamp(linear_x, -limit, limit), clamp(angular_z, -limit, limit)


def normalize_wheel_speeds(
    left: float,
    right: float,
    limit: float = 1.0,
) -> tuple[float, float]:
    """Scale wheel speeds so neither magnitude exceeds the configured limit."""
    if limit <= 0:
        raise ValueError('Wheel-speed limit must be greater than zero.')

    scale = max(1.0, abs(left) / limit, abs(right) / limit)
    return left / scale, right / scale


def build_wheel_command(
    linear_x: float,
    angular_z: float,
    limit: float = 1.0,
) -> tuple[float, float]:
    """Mix linear and angular commands into normalized wheel speeds."""
    left = linear_x - angular_z
    right = linear_x + angular_z
    return normalize_wheel_speeds(left, right, limit=limit)
