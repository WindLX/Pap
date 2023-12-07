use crate::model::{Node, Spring, Vector, VECTOR_ZERO};
use serde::{Deserialize, Serialize};
use std::{cell::RefCell, rc::Rc};
use wasm_bindgen::prelude::wasm_bindgen;
use wasm_bindgen::prelude::JsValue;
use wasm_bindgen::JsError;

#[derive(Debug)]
pub struct System {
    pub nodes: Vec<Rc<RefCell<Node>>>,
    springs: Vec<Rc<Spring>>,
    mu: f32,
    max_x: f32,
    max_y: f32,
    md_radius: f32,
    res_radius: f32,
}

impl System {
    pub fn new(
        nodes: Vec<Node>,
        springs: Vec<Spring>,
        mu: f32,
        max_x: f32,
        max_y: f32,
        md_radius: f32,
        res_radius: f32,
    ) -> Self {
        Self {
            nodes: nodes
                .into_iter()
                .map(|n| Rc::new(RefCell::new(n)))
                .collect(),
            springs: springs.into_iter().map(Rc::new).collect(),
            mu,
            max_x,
            max_y,
            md_radius,
            res_radius,
        }
    }

    pub fn set_pos(&mut self, node_id: usize, pos: Vector) {
        self.nodes[node_id].borrow_mut().pos = pos;
        self.nodes[node_id].borrow_mut().vel = VECTOR_ZERO;
    }

    pub fn step(&mut self) {
        let mut forces = vec![VECTOR_ZERO; self.nodes.len()];
        for spring in &self.springs {
            let node_s = self.nodes[spring.source].clone();
            let node_t = self.nodes[spring.target].clone();
            let force = spring.calc_force([&node_s.borrow(), &node_t.borrow()]);
            forces[spring.source] = force;
            forces[spring.target] = -force;
        }
        for (i, node) in self.nodes.iter().enumerate() {
            let mut force = VECTOR_ZERO;
            for (ii, nn) in self.nodes.iter().enumerate() {
                if ii != i {
                    force += node.borrow().calc_gravitation(&nn.borrow());
                }
            }
            let fi = node.borrow().vel.cof_mul(self.mu);
            force -= fi;
            forces[i] += force;
            let radius = if node.borrow().is_md {
                self.md_radius
            } else {
                self.res_radius
            };
            if node.borrow().pos.x > self.max_x - radius || node.borrow().pos.x < radius {
                node.borrow_mut().vel.x *= -1.0;
            }
            if node.borrow().pos.y > self.max_y - radius || node.borrow().pos.y < radius {
                node.borrow_mut().vel.y *= -1.0;
            }
        }
        self.nodes
            .iter()
            .enumerate()
            .for_each(|(i, n)| n.borrow_mut().step(forces[i]))
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsNode {
    data: String,
    is_md: bool,
    pos: Vector,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsLink {
    source: usize,
    target: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsConfig {
    pub origin_x: f32,
    pub origin_y: f32,
    pub max_x: f32,
    pub max_y: f32,
    pub md_radius: f32,
    pub res_radius: f32,
    pub md_length: f32,
    pub res_length: f32,
    pub stiffness: f32,
    pub gravitation_weight: f32,
    pub gravitation_bais: f32,
    pub md_mass: f32,
    pub res_mass: f32,
    pub mu: f32,
}

#[derive(Debug)]
#[wasm_bindgen]
pub struct JsSystem {
    system: System,
}

#[wasm_bindgen]
impl JsSystem {
    pub fn new(
        nodes: Vec<JsValue>,
        links: Vec<JsValue>,
        config: JsValue,
    ) -> Result<JsSystem, JsError> {
        let config: JsConfig = serde_wasm_bindgen::from_value(config)?;
        let nodes: Vec<Node> = nodes
            .iter()
            .map(|node| {
                let node: JsNode = serde_wasm_bindgen::from_value(node.clone()).unwrap();
                let mass = if node.is_md {
                    config.md_mass
                } else {
                    config.res_mass
                };
                Node::new(
                    node.is_md,
                    config.gravitation_weight,
                    config.gravitation_bais,
                    mass,
                    Vector::new(config.origin_x, config.origin_y),
                )
            })
            .collect();
        let links: Vec<Spring> = links
            .iter()
            .map(|link| {
                let link: JsLink = serde_wasm_bindgen::from_value(link.clone()).unwrap();
                if nodes[link.target as usize].is_md {
                    Spring::new(config.md_length, config.stiffness, link.source, link.target)
                } else {
                    Spring::new(
                        config.res_length,
                        config.stiffness,
                        link.source,
                        link.target,
                    )
                }
            })
            .collect();
        Ok(JsSystem {
            system: System::new(
                nodes,
                links,
                config.mu,
                config.max_x,
                config.max_y,
                config.md_radius,
                config.res_radius,
            ),
        })
    }

    pub fn set_pos(&mut self, node_id: usize, pos: JsValue) {
        let pos = serde_wasm_bindgen::from_value(pos).unwrap();
        self.system.set_pos(node_id, pos)
    }

    pub fn step(&mut self) -> Vec<JsValue> {
        self.system.step();
        self.system
            .nodes
            .iter()
            .map(|n| {
                let vec = &n.borrow().pos;
                serde_wasm_bindgen::to_value(vec).unwrap()
            })
            .collect()
    }
}
