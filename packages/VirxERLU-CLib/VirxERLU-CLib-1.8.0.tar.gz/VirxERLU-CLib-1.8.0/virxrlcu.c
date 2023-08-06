#include <math.h>
#include <Python.h>

// Constants

static const double jump_max_duration = 0.2;
static const double jump_speed = 291 + (2 / 3);
static const double jump_acc = 1458 + (1 / 3);
static const double boost_consumption = 33. + (1. / 3.);
static const double max_speed = 2300;
static const double simulation_dt = 1. / 30.;

// Vector stuff

double cap(double value, double min, double max)
{
    if (value < min)
        return min;
    if (value > max)
        return max;
    return value;
};

typedef struct vector
{
    double x;
    double y;
    double z;
} Vector;

struct opti_norm
{
    Vector vector;
    double magnitude;
};

Vector add(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x + vec2.x, vec1.y + vec2.y, vec1.z + vec2.z};
}

Vector sub(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x - vec2.x, vec1.y - vec2.y, vec1.z - vec2.z};
}

Vector multiply(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x * vec2.x, vec1.y * vec2.y, vec1.z * vec2.z};
}

Vector divide(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x / vec2.x, vec1.y / vec2.y, vec1.z / vec2.z};
}

double dot(Vector vec1, Vector vec2)
{
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z;
}

double magnitude(Vector vec)
{
    return sqrt(dot(vec, vec));
}

struct opti_norm normalize(Vector vec)
{
    struct opti_norm r;
    r.vector = (Vector){0, 0, 0};
    r.magnitude = magnitude(vec);

    if (r.magnitude != 0)
        r.vector = (Vector){vec.x / r.magnitude, vec.y / r.magnitude, vec.z / r.magnitude};

    return r;
}

Vector flatten(Vector vec)
{
    return (Vector){vec.x, vec.y, 0};
}

double angle(Vector vec1, Vector vec2)
{
    return acos(cap(dot(normalize(vec1).vector, normalize(vec2).vector), -1, 1));
}

Vector cross(Vector vec1, Vector vec2)
{
    return (Vector){(vec1.y * vec2.z) - (vec1.z * vec2.y), (vec1.z * vec2.x) - (vec1.x * vec2.z), (vec1.x * vec2.y) - (vec1.y * vec2.x)};
}

Vector double_to_vector(double num)
{
    return (Vector){num, num, num};
}

Vector clamp2D(Vector vec, Vector start, Vector end)
{
    Vector s = normalize(vec).vector;
    _Bool right = dot(s, cross(end, (Vector){0, 0, -1})) < 0;
    _Bool left = dot(s, cross(start, (Vector){0, 0, -1})) > 0;

    if ((dot(end, cross(start, (Vector){0, 0, -1})) > 0) ? (right && left) : (right || left))
        return vec;

    if (dot(start, s) < dot(end, s))
        return end;

    return start;
}

Vector clamp(Vector vec, Vector start, Vector end)
{
    Vector s = clamp2D(vec, start, end);
    double start_z = min(start.z, end.z);
    double end_z = max(start.z, end.z);

    if (s.z < start_z)
        s.z = start_z;
    else if (s.z > end_z)
        s.z = end_z;

    return s;
}

double dist(Vector vec1, Vector vec2)
{
    return magnitude(sub(vec1, vec2));
}

// Main lib

struct jump_shot
{
    int found;
    Vector best_shot_vector;
};

struct aerial_shot
{
    int found;
    Vector ball_intercept;
};

struct post_correction
{
    Vector left;
    Vector right;
    _Bool swapped;
};

struct post_correction correct_for_posts(Vector ball_location, Vector left_target, Vector right_target)
{
    double ball_radius = 120;
    Vector goal_line_perp = cross(sub(right_target, left_target), (Vector){0, 0, 1});
    Vector left = add(left_target, cross(normalize(sub(left_target, ball_location)).vector, multiply((Vector){0, 0, 1}, double_to_vector(ball_radius))));
    Vector right = add(right_target, cross(normalize(sub(right_target, ball_location)).vector, multiply((Vector){0, 0, 1}, double_to_vector(ball_radius))));

    struct post_correction r;
    r.left = (dot(sub(left, left_target), goal_line_perp) > 0) ? left_target : left;
    r.right = (dot(sub(right, right_target), goal_line_perp) > 0) ? right_target : right;
    r.swapped = dot(cross(normalize(sub(left, ball_location)).vector, (Vector){0, 0, 1}), normalize(sub(right, ball_location)).vector) > -0.1;

    return r;
};

_Bool in_field(Vector point, int radius)
{
    point = (Vector){fabs(point.x), fabs(point.y), fabs(point.z)};
    return !((point.x > 4080 - radius) || (point.y > 5900 - radius) || (point.x > 880 - radius && point.y > 5105 - radius) || (point.x > 2650 && point.y > -point.x + 8025 - radius));
};

double find_slope(Vector shot_vector, Vector car_to_target)
{
    double d = dot(shot_vector, car_to_target);
    double e = fabs(dot(cross(shot_vector, (Vector){0, 0, 1}), car_to_target));

    if (e == 0)
        return 10 * copysign(1, d);

    return max(min(d / e, 3), -3);
};

double throttle_acceleration(double car_velocity_x)
{
    if (car_velocity_x >= 1410)
        return 0;

    double x0, y0, x1, y1;
    if (car_velocity_x < 1400) {
        x0 = 0;
        y0 = 1600;
        x1 = 1400;
        y1 = 160;
    } else {
        x0 = 1400;
        y0 = 160;
        x1 = 1410;
        y1 = 0;
    }

    return y0 + ((y1-y0)/(x1-x0)) * (car_velocity_x - x0);
}

double car_drive_to_target_simulation(double boost_accel, double car_to_target, double car_speed, int car_boost)
{
    double b = car_boost;
    double t = 0;
    double v = car_speed;
    double d = car_to_target;
    _Bool b_a;

    while (d > 50) {
        b_a = 0;

        if (b > boost_consumption * simulation_dt && v < max_speed - (boost_accel * simulation_dt)) {
            b_a = 1;
            v += boost_accel * simulation_dt;
            b -= boost_consumption * simulation_dt;
        }

        v += throttle_acceleration(v) * simulation_dt;

        d -= v * simulation_dt;
        t += simulation_dt;
    }

    return t;
}

double car_turn_simulation(double turning_time, double car_speed)
{
    double t = turning_time;
    double v = car_speed;
    
    while (t >= simulation_dt) {
        if (v > 1410)
            v -= 100 * simulation_dt;

        v += throttle_acceleration(v) * simulation_dt;
        t -= simulation_dt;
    }

    return v;
}

struct jump_shot parse_slice_for_jump_shot_with_target(double time_remaining, double best_shot_value, Vector ball_location, Vector car_location, Vector car_forward, int car_boost, Vector left_target, Vector right_target, double boost_accel, double car_speed)
{
    struct jump_shot r;
    r.found = -1;

    Vector car_to_ball = sub(ball_location, car_location);
    struct opti_norm car_to_ball_norm = normalize(car_to_ball);
    Vector direction = car_to_ball_norm.vector;
    double distance = car_to_ball_norm.magnitude;

    double forward_angle = angle(flatten(direction), flatten(car_forward));
    double backward_angle = Py_MATH_PIl - forward_angle;

    double forward_turn_time = forward_angle * 0.318;
    double backward_turn_time = backward_angle * 0.418;

    double forward_time = time_remaining - forward_turn_time;
    double backward_time = time_remaining - backward_turn_time;

    _Bool forward_flag = forward_time > 0 && forward_time > car_drive_to_target_simulation(boost_accel, distance, car_turn_simulation(forward_turn_time, car_speed), car_boost);
    _Bool backward_flag = backward_time > 0 && distance < 1500 && backward_time > car_drive_to_target_simulation(boost_accel, distance, car_turn_simulation(backward_turn_time, car_speed), 0);

    if (forward_flag || backward_flag)
    {
        struct post_correction pst_crrctn = correct_for_posts(ball_location, left_target, right_target);
        if (!pst_crrctn.swapped)
        {
            Vector left_vector = normalize(sub(pst_crrctn.left, ball_location)).vector;
            Vector right_vector = normalize(sub(pst_crrctn.right, ball_location)).vector;
            r.best_shot_vector = clamp(direction, left_vector, right_vector);

            if (in_field(sub(ball_location, multiply(r.best_shot_vector, double_to_vector(best_shot_value))), 1))
            {
                double slope = find_slope(r.best_shot_vector, car_to_ball);
                if ((forward_flag && slope > 0) || (backward_flag && slope > 0.5))
                    r.found = 1;
            }
        }
    }

    return r;
};

struct jump_shot parse_slice_for_jump_shot(double time_remaining, double best_shot_value, Vector ball_location, Vector car_location, Vector car_forward, int car_boost, double boost_accel, double car_speed)
{
    struct jump_shot r;
    r.found = -1;

    Vector car_to_ball = sub(ball_location, car_location);
    struct opti_norm car_to_ball_norm = normalize(car_to_ball);
    Vector direction = car_to_ball_norm.vector;
    double distance = car_to_ball_norm.magnitude;

    double forward_angle = angle(flatten(direction), flatten(car_forward));
    double backward_angle = Py_MATH_PIl - forward_angle;

    double forward_turn_time = forward_angle * 0.318;
    double backward_turn_time = backward_angle * 0.418;

    double forward_time = time_remaining - forward_turn_time;
    double backward_time = time_remaining - backward_turn_time;

    _Bool forward_flag = forward_time > 0 && forward_time > car_drive_to_target_simulation(boost_accel, distance, car_turn_simulation(forward_turn_time, car_speed), car_boost);
    _Bool backward_flag = backward_time > 0 && distance < 1500 && backward_time > car_drive_to_target_simulation(boost_accel, distance, car_turn_simulation(backward_turn_time, car_speed), 0);

    r.best_shot_vector = direction;

    if ((forward_flag || backward_flag) && in_field(sub(ball_location, multiply(r.best_shot_vector, double_to_vector(best_shot_value))), 1))
    {
        double slope = find_slope(r.best_shot_vector, car_to_ball);
        if ((forward_flag && slope > 0) || (backward_flag && slope > 0.5))
            r.found = 1;
    }

    return r;
};

struct jump_shot parse_slice_for_double_jump_with_target(double time_remaining, double best_shot_value, Vector ball_location, Vector car_location, Vector car_forward, int car_boost, Vector left_target, Vector right_target, double boost_accel, double car_speed)
{
    struct jump_shot r;
    r.found = -1;

    Vector car_to_ball = sub(ball_location, car_location);
    struct opti_norm car_to_ball_norm = normalize(car_to_ball);
    Vector direction = car_to_ball_norm.vector;
    double distance = car_to_ball_norm.magnitude;

    double forward_turn_time = angle(flatten(direction), flatten(car_forward)) * 0.318;
    double forward_time = time_remaining - forward_turn_time;

    if (forward_time > 0 && forward_time > car_drive_to_target_simulation(boost_accel, distance, car_turn_simulation(forward_turn_time, car_speed), car_boost))
    {
        struct post_correction pst_crrctn = correct_for_posts(ball_location, left_target, right_target);
        if (!pst_crrctn.swapped)
        {
            Vector left_vector = normalize(sub(pst_crrctn.left, ball_location)).vector;
            Vector right_vector = normalize(sub(pst_crrctn.right, ball_location)).vector;
            r.best_shot_vector = clamp2D(direction, left_vector, right_vector);

            if (in_field(sub(ball_location, multiply(r.best_shot_vector, double_to_vector(best_shot_value))), 1) && find_slope(r.best_shot_vector, car_to_ball) > 0)
                r.found = 1;
        }
    }

    return r;
};

struct jump_shot parse_slice_for_double_jump(double time_remaining, double best_shot_value, Vector ball_location, Vector car_location, Vector car_forward, int car_boost, double boost_accel, double car_speed)
{
    struct jump_shot r;
    r.found = -1;

    Vector car_to_ball = sub(ball_location, car_location);
    struct opti_norm car_to_ball_norm = normalize(car_to_ball);
    Vector direction = car_to_ball_norm.vector;
    double distance = car_to_ball_norm.magnitude;

    double forward_turn_time = angle(flatten(direction), flatten(car_forward)) * 0.318;
    double forward_time = time_remaining - forward_turn_time;

    r.best_shot_vector = direction;

    if (forward_time > 0 && in_field(sub(ball_location, multiply(r.best_shot_vector, double_to_vector(best_shot_value))), 1) && forward_time > car_drive_to_target_simulation(boost_accel, distance, car_turn_simulation(forward_turn_time, car_speed), car_boost))
        r.found = 1;

    return r;
};

struct car
{
    Vector location;
    Vector velocity;
    Vector up;
    Vector forward;
    int airborne;
    int boost;
};

_Bool is_viable(double time_remaining, double hitbox_height, double boost_accel, Vector gravity, struct car me, Vector target)
{
    Vector T = double_to_vector(time_remaining);
    Vector xf = add(add(me.location, multiply(me.velocity, T)), multiply(multiply(multiply(double_to_vector(0.5), gravity), T), T));
    Vector vf = add(me.velocity, multiply(gravity, T));

    _Bool ceiling = me.location.z > 2044 - hitbox_height;

    if (me.airborne == -1 && !ceiling)
    {
        xf = add(xf, multiply(me.up, double_to_vector(jump_speed * (2 * time_remaining - jump_max_duration) + jump_acc * (time_remaining * jump_max_duration - 0.5 * jump_max_duration * jump_max_duration))));
        vf = add(vf, multiply(me.up, double_to_vector(2 * jump_speed + jump_acc * jump_max_duration)));
    }

    if (ceiling)
        target.z -= 92;

    Vector delta_x = sub(target, xf);
    Vector f = normalize(delta_x).vector;

    double phi = angle(delta_x, me.forward);
    double turn_time = 0.7 * (2 * sqrt(phi / 9));
    double tau1 = turn_time * cap(1 - 0.3 / phi, 0, 1);
    double required_acc = (2 * magnitude(delta_x) / ((time_remaining - tau1) * (time_remaining - tau1)));
    double ratio = required_acc / boost_accel;
    double tau2 = time_remaining - (time_remaining - tau1) * sqrt(1 - cap(ratio, 0, 1));
    double boost_estimate = (tau2 - tau1) * 30;

    Vector velocity_estimate = add(vf, multiply(f, double_to_vector(boost_accel * (tau2 - tau1))));

    _Bool enough_boost = boost_estimate < 0.95 * me.boost;
    _Bool enough_time = fabs(ratio) < 0.9;
    _Bool enough_speed = magnitude(velocity_estimate) < 0.9 * max_speed;

    return enough_speed && enough_boost && enough_time;
};

struct aerial_shot parse_slice_for_aerial_shot_with_target(double time_remaining, double best_shot_value, double boost_accel, Vector gravity, Vector ball_location, struct car me, Vector left_target, Vector right_target)
{
    struct aerial_shot r;
    r.found = -1;

    Vector car_to_ball = sub(ball_location, me.location);
    Vector direction = normalize(car_to_ball).vector;

    struct post_correction pst_crrctn = correct_for_posts(ball_location, left_target, right_target);
    if (!pst_crrctn.swapped)
    {
        Vector left_vector = normalize(sub(pst_crrctn.left, ball_location)).vector;
        Vector right_vector = normalize(sub(pst_crrctn.right, ball_location)).vector;
        r.ball_intercept = sub(ball_location, multiply(clamp(direction, left_vector, right_vector), double_to_vector(best_shot_value)));

        if (in_field(r.ball_intercept, 1))
        {
            double slope = find_slope(r.ball_intercept, car_to_ball);
            if (slope > 0 && is_viable(time_remaining, ceil(best_shot_value - 92.75) * 2, boost_accel, gravity, me, r.ball_intercept))
                r.found = 1;
        }
    }

    return r;
};

struct aerial_shot parse_slice_for_aerial_shot(double time_remaining, double best_shot_value, double boost_accel, Vector gravity, Vector ball_location, struct car me)
{
    struct aerial_shot r;
    r.found = -1;

    Vector car_to_ball = sub(ball_location, me.location);
    r.ball_intercept = sub(ball_location, multiply(normalize(car_to_ball).vector, double_to_vector(best_shot_value)));

    if (in_field(r.ball_intercept, 1))
    {
        double slope = find_slope(r.ball_intercept, car_to_ball);
        if (slope > 0 && is_viable(time_remaining, ceil(best_shot_value - 92.75) * 2, boost_accel, gravity, me, r.ball_intercept))
            r.found = 1;
    }

    return r;
};

static PyObject *method_parse_slice_for_jump_shot_with_target(PyObject *self, PyObject *args)
{
    int car_boost;
    double time_remaining, best_shot_value, boost_accel, car_speed, cap_;
    Vector ball_location, car_location, car_forward, left_target, right_target;

    // new args are for >=1.8
    if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id(ddd)(ddd)", &time_remaining, &best_shot_value, &boost_accel, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &car_speed, &left_target.x, &left_target.y, &left_target.z, &right_target.x, &right_target.y, &right_target.z)) {
        // old args are for <1.8 and >=1.7
        // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
        PyErr_Clear();
        if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i(ddd)(ddd)d", &time_remaining, &best_shot_value, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &left_target.x, &left_target.y, &left_target.z, &right_target.x, &right_target.y, &right_target.z, &cap_))
            return NULL;

        boost_accel = 991. + (2. / 3.);
        car_speed = 0;
    }

    struct jump_shot data_struct = parse_slice_for_jump_shot_with_target(time_remaining, best_shot_value, ball_location, car_location, car_forward, car_boost, left_target, right_target, boost_accel, car_speed);

    return Py_BuildValue("{s:i,s:(ddd)}", "found", data_struct.found, "best_shot_vector", data_struct.best_shot_vector.x, data_struct.best_shot_vector.y, data_struct.best_shot_vector.z);
};

static PyObject *method_parse_slice_for_jump_shot(PyObject *self, PyObject *args)
{
    int car_boost;
    double time_remaining, best_shot_value, boost_accel, car_speed, cap_;
    Vector ball_location, car_location, car_forward;

    // new args are for >=1.8
    if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id", &time_remaining, &best_shot_value, &boost_accel, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &car_speed)) {
        // old args are for <1.8 and >=1.7
        // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
        PyErr_Clear();
        if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i|d", &time_remaining, &best_shot_value, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &cap_))
            return NULL;
        
        boost_accel = 991. + (2. / 3.);
        car_speed = 0;

    }
    struct jump_shot data_struct = parse_slice_for_jump_shot(time_remaining, best_shot_value, ball_location, car_location, car_forward, car_boost, boost_accel, car_speed);

    return Py_BuildValue("{s:i,s:(ddd)}", "found", data_struct.found, "best_shot_vector", data_struct.best_shot_vector.x, data_struct.best_shot_vector.y, data_struct.best_shot_vector.z);
};

static PyObject *method_parse_slice_for_double_jump_with_target(PyObject *self, PyObject *args)
{
    int car_boost;
    double time_remaining, best_shot_value, boost_accel, car_speed, cap_;
    Vector ball_location, car_location, car_forward, left_target, right_target;

    // new args are for >=1.8
    if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id(ddd)(ddd)", &time_remaining, &best_shot_value, &boost_accel, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &car_speed, &left_target.x, &left_target.y, &left_target.z, &right_target.x, &right_target.y, &right_target.z)) {
        // old args are for <1.8 and >=1.7
        // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
        PyErr_Clear();
        if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i(ddd)(ddd)|d", &time_remaining, &best_shot_value, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &left_target.x, &left_target.y, &left_target.z, &right_target.x, &right_target.y, &right_target.z, &cap_))
            return NULL;
        
        boost_accel = 991. + (2. / 3.);
        car_speed = 0;
    }

    struct jump_shot data_struct = parse_slice_for_double_jump_with_target(time_remaining, best_shot_value, ball_location, car_location, car_forward, car_boost, left_target, right_target, boost_accel, car_speed);

    return Py_BuildValue("{s:i,s:(ddd)}", "found", data_struct.found, "best_shot_vector", data_struct.best_shot_vector.x, data_struct.best_shot_vector.y, data_struct.best_shot_vector.z);
};

static PyObject *method_parse_slice_for_double_jump(PyObject *self, PyObject *args)
{
    int car_boost;
    double time_remaining, best_shot_value, boost_accel, car_speed, cap_;
    Vector ball_location, car_location, car_forward;

    // new args are for >=1.8
    if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id", &time_remaining, &best_shot_value, &boost_accel, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &car_speed)) {
        // old args are for <1.8 and >=1.7
        // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
        PyErr_Clear();
        if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i|d", &time_remaining, &best_shot_value, &ball_location.x, &ball_location.y, &ball_location.z, &car_location.x, &car_location.y, &car_location.z, &car_forward.x, &car_forward.y, &car_forward.z, &car_boost, &cap_))
            return NULL;
        
        boost_accel = 991. + (2. / 3.);
        car_speed = 0;
    }

    struct jump_shot data_struct = parse_slice_for_double_jump(time_remaining, best_shot_value, ball_location, car_location, car_forward, car_boost, boost_accel, car_speed);

    return Py_BuildValue("{s:i,s:(ddd)}", "found", data_struct.found, "best_shot_vector", data_struct.best_shot_vector.x, data_struct.best_shot_vector.y, data_struct.best_shot_vector.z);
};

static PyObject *method_parse_slice_for_aerial_shot_with_target(PyObject *self, PyObject *args)
{
    struct car me;
    double time_remaining, best_shot_value, boost_accel, cap_;
    Vector gravity, ball_location, left_target, right_target;

    // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
    if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)((ddd)(ddd)(ddd)(ddd)ii)(ddd)(ddd)|d", &time_remaining, &best_shot_value, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &ball_location.x, &ball_location.y, &ball_location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.up.x, &me.up.y, &me.up.z, &me.forward.x, &me.forward.y, &me.forward.z, &me.airborne, &me.boost, &left_target.x, &left_target.y, &left_target.z, &right_target.x, &right_target.y, &right_target.z, &cap_))
        return NULL;

    struct aerial_shot data_struct = parse_slice_for_aerial_shot_with_target(time_remaining, best_shot_value, boost_accel, gravity, ball_location, me, left_target, right_target);

    return Py_BuildValue("{s:i,s:(ddd)}", "found", data_struct.found, "ball_intercept", data_struct.ball_intercept.x, data_struct.ball_intercept.y, data_struct.ball_intercept.z);
};

static PyObject *method_parse_slice_for_aerial_shot(PyObject *self, PyObject *args)
{
    struct car me;
    double time_remaining, best_shot_value, boost_accel, cap_;
    Vector gravity, ball_location;

    // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
    if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)((ddd)(ddd)(ddd)(ddd)ii)|d", &time_remaining, &best_shot_value, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &ball_location.x, &ball_location.y, &ball_location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.up.x, &me.up.y, &me.up.z, &me.forward.x, &me.forward.y, &me.forward.z, &me.airborne, &me.boost, &cap_))
        return NULL;

    struct aerial_shot data_struct = parse_slice_for_aerial_shot(time_remaining, best_shot_value, boost_accel, gravity, ball_location, me);

    return Py_BuildValue("{s:i,s:(ddd)}", "found", data_struct.found, "ball_intercept", data_struct.ball_intercept.x, data_struct.ball_intercept.y, data_struct.ball_intercept.z);
};

static PyMethodDef methods[] = {
    {"parse_slice_for_jump_shot_with_target", method_parse_slice_for_jump_shot_with_target, METH_VARARGS, "Parse slice for a jump shot with a target"},
    {"parse_slice_for_jump_shot", method_parse_slice_for_jump_shot, METH_VARARGS, "Parse slice for a jump shot"},
    {"parse_slice_for_double_jump_with_target", method_parse_slice_for_double_jump_with_target, METH_VARARGS, "Parse slice for a double jump with a target"},
    {"parse_slice_for_double_jump", method_parse_slice_for_double_jump, METH_VARARGS, "Parse slice for a double jump"},
    {"parse_slice_for_aerial_shot_with_target", method_parse_slice_for_aerial_shot_with_target, METH_VARARGS, "Parse slice for an aerial shot with a target"},
    {"parse_slice_for_aerial_shot", method_parse_slice_for_aerial_shot, METH_VARARGS, "Parse slice for an aerial shot"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "virxrlcu",
    "C Library for VirxERLU",
    -1,
    methods};

PyMODINIT_FUNC PyInit_virxrlcu(void)
{
    return PyModule_Create(&module);
};