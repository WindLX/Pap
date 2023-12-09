import { BaseSchema } from "./base"

type Vector = {
    x: number,
    y: number
}

interface NetSchema extends BaseSchema {
    nodes: NetNodeSchema[],
    links: NetLinkSchema[],
}

interface NetNodeSchema extends BaseSchema {
    id: number,
    data: string,
    is_md: boolean,
    pos: Vector
}

interface NetLinkSchema extends BaseSchema {
    source: number,
    target: number,
}

type NetConfig = {
    origin_x: number,
    origin_y: number,
    max_x: number,
    max_y: number,
    md_radius: number,
    res_radius: number,
    md_length: number,
    res_length: number,
    stiffness: number,
    gravitation_weight: number,
    gravitation_bais: number,
    md_mass: number,
    res_mass: number,
    mu: number,
}

export type {
    Vector, NetSchema, NetConfig, NetLinkSchema, NetNodeSchema
}
