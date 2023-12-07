use md_parser::generator::NetGenerator;
use std::collections::HashSet;
use std::fs;

#[derive(Debug, Clone)]
pub struct NoteSchema {
    id: usize,
    name: String,
    url: String,
}

impl NoteSchema {
    pub fn new(id: usize, name: String, url: String) -> Self {
        Self { id, name, url }
    }
}

#[derive(Debug, Clone)]
pub struct Vector {
    pub x: usize,
    pub y: usize,
}

#[derive(Debug, Clone)]
pub struct NetNodeSchema {
    pub id: usize,
    pub data: String,
    pub is_md: bool,
    pub pos: Vector,
}

#[derive(Debug, Clone, Hash)]
pub struct NetLinkSchema {
    pub source: usize,
    pub target: usize,
}

impl PartialEq for NetLinkSchema {
    fn eq(&self, other: &Self) -> bool {
        (self.source == other.source && self.target == other.target)
            || (self.source == other.target && self.target == other.source)
    }
}

impl Eq for NetLinkSchema {}

#[derive(Debug, Clone)]
pub struct NetSchema {
    pub nodes: Vec<NetNodeSchema>,
    pub links: Vec<NetLinkSchema>,
}

pub struct MultiNetGenerator;

impl MultiNetGenerator {
    pub fn new() -> Self {
        Self
    }

    pub fn generate(&self, notes: Vec<NoteSchema>) -> NetSchema {
        let mut nodes: Vec<NetNodeSchema> = notes
            .iter()
            .map(|n| NetNodeSchema {
                id: n.id,
                data: n.name.clone(),
                is_md: true,
                pos: Vector { x: 0, y: 0 },
            })
            .collect();
        let mut link_set: HashSet<NetLinkSchema> = HashSet::new();
        for note in notes {
            let input = fs::read_to_string(note.url).unwrap();
            let links = self.get_refs(input);
            links.iter().for_each(|l| {
                match &l.href {
                    Some(h) => {
                        if !l.is_md {
                            nodes.push(NetNodeSchema {
                                id: 0,
                                data: l.content.clone(),
                                is_md: false,
                                pos: Vector { x: 0, y: 0 },
                            });
                            link_set.insert(NetLinkSchema {
                                source: note.id,
                                target: nodes.len() - 1,
                            });
                        } else {
                            let idx = nodes.iter().position(|n| {
                                let name = &h[5..];
                                n.data == name
                            });
                            if let Some(idx) = idx {
                                link_set.insert(NetLinkSchema {
                                    source: note.id,
                                    target: idx,
                                });
                            }
                        }
                    }
                    None => (),
                };
            })
        }
        NetSchema {
            nodes,
            links: link_set.into_iter().collect(),
        }
    }
}

impl NetGenerator for MultiNetGenerator {}
