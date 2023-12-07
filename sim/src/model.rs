use serde::{Deserialize, Serialize};
use std::ops::{Add, AddAssign, Neg, Sub, SubAssign};
use web_sys::js_sys::Math;

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct Vector {
    pub x: f32,
    pub y: f32,
}

impl PartialEq for Vector {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}

impl Eq for Vector {}

pub const VECTOR_ZERO: Vector = Vector { x: 0.0, y: 0.0 };
pub const VECTOR_UP: Vector = Vector { x: 0.0, y: 1.0 };
pub const VECTOR_RIGHT: Vector = Vector { x: 1.0, y: 0.0 };

impl Vector {
    pub fn new(x: f32, y: f32) -> Vector {
        Self { x, y }
    }

    pub fn delta() -> Vector {
        Vector {
            x: 0.001 * Math::random() as f32,
            y: 0.001 * Math::random() as f32,
        }
    }

    pub fn unit(&self) -> Vector {
        Vector {
            x: self.x / self.norm(),
            y: self.y / self.norm(),
        }
    }

    pub fn norm(self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt() as f32
    }

    pub fn norm_sq(self) -> f32 {
        self.x.powi(2) + self.y.powi(2)
    }

    pub fn distance(self, other: Self) -> f32 {
        (self - other).norm()
    }

    pub fn dot(self, other: Self) -> f32 {
        self.x * other.x + self.y * other.y
    }

    pub fn cof_mul(self, coefficient: f32) -> Self {
        Self {
            x: self.x * coefficient,
            y: self.y * coefficient,
        }
    }

    pub fn cof_div(self, coefficient: f32) -> Self {
        Self {
            x: self.x / coefficient,
            y: self.y / coefficient,
        }
    }
}

impl Add for Vector {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

impl AddAssign for Vector {
    fn add_assign(&mut self, rhs: Self) {
        self.x += rhs.x;
        self.y += rhs.y;
    }
}

impl Sub for Vector {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        Self {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
        }
    }
}

impl SubAssign for Vector {
    fn sub_assign(&mut self, rhs: Self) {
        self.x -= rhs.x;
        self.y -= rhs.y;
    }
}

impl Neg for Vector {
    type Output = Self;
    fn neg(self) -> Self::Output {
        Self {
            x: -self.x,
            y: -self.y,
        }
    }
}

#[derive(Debug, Clone)]
pub struct Node {
    pub is_md: bool,
    gravitation_weight: f32,
    gravitation_bais: f32,
    mass: f32,
    pub pos: Vector,
    pub vel: Vector,
}

impl Node {
    pub fn new(
        is_md: bool,
        gravitation_weight: f32,
        gravitation_bais: f32,
        mass: f32,
        pos: Vector,
    ) -> Self {
        Self {
            is_md,
            gravitation_bais,
            gravitation_weight,
            mass,
            pos,
            vel: VECTOR_ZERO,
        }
    }

    pub fn step(&mut self, force: Vector) {
        let accel = force.cof_div(self.mass);
        let last_vel = self.vel.clone();
        self.vel += accel.cof_mul(0.02);
        self.pos += (self.vel + last_vel).cof_div(2.0).cof_mul(0.02);
    }

    pub fn calc_gravitation(&self, other: &Node) -> Vector {
        let mut dist = other.pos - self.pos;
        if dist == VECTOR_ZERO {
            dist = Vector::delta()
        }
        let distance = dist.norm();
        dist.unit().cof_mul(
            self.gravitation_weight * (self.mass * other.mass) * (distance - self.gravitation_bais),
        )
    }
}

#[derive(Debug, Clone)]
pub struct Spring {
    origin_length: f32,
    stiffness: f32,
    pub source: usize,
    pub target: usize,
}

impl Spring {
    pub fn new(origin_length: f32, stiffness: f32, source: usize, target: usize) -> Self {
        Self {
            origin_length,
            stiffness,
            source,
            target,
        }
    }

    pub fn calc_force(&self, nodes: [&Node; 2]) -> Vector {
        let mut dist = nodes[0].pos - nodes[1].pos;
        if dist == VECTOR_ZERO {
            dist = Vector::delta()
        }
        let distance = dist.norm();
        let delta_length = distance - self.origin_length;
        let force = -self.stiffness * delta_length;
        dist.unit().cof_mul(force)
    }
}
