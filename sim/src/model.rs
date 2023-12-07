use serde::{Deserialize, Serialize};
use std::ops::{Add, AddAssign, Sub, SubAssign};

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct Vector {
    x: f32,
    y: f32,
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

    pub fn norm(self) -> f32 {
        (self.x.powf(2.0) + self.y.powf(2.0)).sqrt() as f32
    }

    pub fn norm_sq(self) -> f32 {
        self.x.powf(2.0) + self.y.powf(2.0)
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

#[derive(Debug, Clone)]
pub struct Node {
    gravitation_weight: f32,
    gravitation_bais: f32,
    mass: f32,
    pub pos: Vector,
    vel: Vector,
}

impl Node {
    pub fn new(gravitation_weight: f32, gravitation_bais: f32, mass: f32, pos: Vector) -> Self {
        Self {
            gravitation_bais,
            gravitation_weight,
            mass,
            pos,
            vel: VECTOR_ZERO,
        }
    }

    pub fn step(&mut self, force: Vector) {
        let last_vel = self.vel.clone();
        self.vel += force.cof_mul(self.mass);
        self.pos += (self.vel + last_vel).cof_div(2.0).cof_mul(self.mass);
    }

    pub fn calc_gravitation(&self, other: &Node) -> Vector {
        let dis = other.pos - self.pos;
        let distance = dis.norm();
        dis.cof_mul(distance * self.gravitation_weight + self.gravitation_bais)
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
        let dist = nodes[0].pos - nodes[1].pos;
        let distance = dist.norm();
        let delta_length = distance - self.origin_length;
        let force = self.stiffness * delta_length;
        println!("{:?}", dist.cof_mul(force));
        dist.cof_mul(force)
    }
}
