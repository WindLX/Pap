use std::ops::{AddAssign, SubAssign};

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Vector {
    x: f32,
    y: f32,
}

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

    pub fn dot(self, other: Self) -> f32 {
        self.x * other.x + self.y * other.y
    }
}

impl AddAssign for Vector {
    fn add_assign(&mut self, rhs: Self) {
        self.x += rhs.x;
        self.y += rhs.y;
    }
}

impl SubAssign for Vector {
    fn sub_assign(&mut self, rhs: Self) {
        self.x -= rhs.x;
        self.y -= rhs.y;
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Node {
    id: usize,
    is_md: bool,
    children: Vec<usize>,
    pos: Vector,
    vel: Vector,
}
