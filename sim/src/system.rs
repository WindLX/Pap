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
}

impl System {
    pub fn new(nodes: Vec<Node>, springs: Vec<Spring>) -> Self {
        Self {
            nodes: nodes
                .into_iter()
                .map(|n| Rc::new(RefCell::new(n)))
                .collect(),
            springs: springs.into_iter().map(Rc::new).collect(),
        }
    }

    pub fn step(&mut self) {
        let mut forces = vec![VECTOR_ZERO; self.nodes.len()];
        for spring in &self.springs {
            let node_s = self.nodes[spring.source].clone();
            let node_t = self.nodes[spring.target].clone();
            let force = spring.calc_force([&node_s.borrow(), &node_t.borrow()]);
            // println!("{:?}", force);
            forces[spring.source] = force
        }
        for (i, node) in self.nodes.iter().enumerate() {
            let mut force = VECTOR_ZERO;
            for (ii, nn) in self.nodes.iter().enumerate() {
                if ii != i {
                    force += node.borrow().calc_gravitation(&nn.borrow())
                }
            }
            forces[i] += force;
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
    pub origin_length: f32,
    pub stiffness: f32,
    pub gravitation_weight: f32,
    pub gravitation_bais: f32,
    pub md_mass: f32,
    pub res_mass: f32,
}

#[derive(Debug)]
#[wasm_bindgen]
pub struct JsSystem {
    system: System,
}

const ORIGIN_X: f32 = 50.0;
const ORIGIN_Y: f32 = 50.0;

const ORIGIN_LENGTH: f32 = 50.0;
const STIFFNESS: f32 = 3.0;

const GRAVITIATION_WEIGHT: f32 = 1.0;
const GRAVITIATION_BAIS: f32 = -30.0;
const MD_MASS: f32 = 10.0;
const RES_MASS: f32 = 1.0;

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
                Spring::new(
                    config.origin_length,
                    config.stiffness,
                    link.source,
                    link.target,
                )
            })
            .collect();
        Ok(JsSystem {
            system: System::new(nodes, links),
        })
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
