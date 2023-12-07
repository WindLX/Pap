use sim::{
    model::{Node, Spring, Vector},
    system::{self, JsConfig, JsNode, System},
};

fn main() {
    let config = JsConfig {
        origin_x: 50.0,
        origin_y: 50.0,
        origin_length: 50.0,
        gravitation_bais: -30.0,
        gravitation_weight: 1.0,
        md_mass: 1.0,
        res_mass: 1.0,
        stiffness: 3.0,
    };
    let mass = if true {
        config.md_mass
    } else {
        config.res_mass
    };
    let node = Node::new(
        config.gravitation_weight,
        config.gravitation_bais,
        mass,
        Vector::new(config.origin_x, config.origin_y),
    );
    let nodes = vec![node.clone(), node.clone(), node.clone(), node.clone()];
    let links = vec![[0, 1], [0, 2], [0, 3]];
    let links: Vec<Spring> = links
        .iter()
        .map(|link| Spring::new(config.origin_length, config.stiffness, link[0], link[1]))
        .collect();

    let mut system = System::new(nodes, links);

    system.step();
    let res: Vec<Vector> = system
        .nodes
        .iter()
        .map(|n| {
            let vec = &n.borrow().pos;
            vec.clone()
        })
        .collect();

    println!("{:?}", res);
}
