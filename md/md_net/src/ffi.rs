use crate::net::*;
use std::{
    ffi::{c_char, c_uint, CStr, CString},
    mem::size_of,
};

#[repr(C)]
pub struct CNoteSchema {
    id: c_uint,
    name: *const libc::c_char,
    url: *const libc::c_char,
}

#[repr(C)]
pub struct CNoteSchemaVec {
    notes: *const CNoteSchema,
    len: c_uint,
}

#[repr(C)]
pub struct CNetNodeSchema {
    id: c_uint,
    data: *const libc::c_char,
    is_md: c_uint,
    pos_x: c_uint,
    pox_y: c_uint,
}

#[repr(C)]
pub struct CNetLinkSchema {
    source: c_uint,
    target: c_uint,
}

#[repr(C)]
pub struct CNetSchema {
    nodes: *const *const CNetNodeSchema,
    n_len: c_uint,
    links: *const *const CNetLinkSchema,
    l_len: c_uint,
}

#[repr(C)]
pub struct CNetGenerator {
    gen: *const MultiNetGenerator,
}

#[no_mangle]
pub extern "C" fn init_net_generator() -> *const CNetGenerator {
    let net_generator = MultiNetGenerator::new();
    let p = Box::into_raw(Box::new(net_generator));
    Box::into_raw(Box::new(CNetGenerator { gen: p }))
}

#[no_mangle]
pub unsafe extern "C" fn generate(
    net_generator: *const CNetGenerator,
    notes: *const CNoteSchemaVec,
) -> *const CNetSchema {
    let notes = parse_note_schema_vec(notes);
    let net = (*(*net_generator).gen).generate(notes);
    let clink_vec: Vec<*const CNetLinkSchema> =
        net.links.iter().map(|o| copy_net_link_schema(o)).collect();
    let l_len = clink_vec.len();
    let cnode_vec: Vec<*const CNetNodeSchema> =
        net.nodes.iter().map(|o| copy_net_node_schema(o)).collect();
    let n_len = cnode_vec.len();
    let n_p = libc::malloc(n_len * size_of::<*const CNetNodeSchema>());
    let l_p = libc::malloc(l_len * size_of::<*const CNetLinkSchema>());
    std::ptr::copy_nonoverlapping(clink_vec.as_ptr(), l_p.cast(), l_len);
    std::ptr::copy_nonoverlapping(cnode_vec.as_ptr(), n_p.cast(), n_len);
    let p = CNetSchema {
        nodes: n_p as *const *const CNetNodeSchema,
        n_len: n_len as c_uint,
        links: l_p as *const *const CNetLinkSchema,
        l_len: l_len as c_uint,
    };
    Box::into_raw(Box::new(p))
}

#[no_mangle]
pub unsafe extern "C" fn free_net_schema(p: *const CNetSchema) {
    for p in std::slice::from_raw_parts((*p).nodes, (*p).n_len as usize) {
        free_string((*(*p)).data.cast_mut())
    }
    libc::free((*p).links as *mut libc::c_void);
    libc::free((*p).nodes as *mut libc::c_void);
}

pub unsafe fn copy_net_node_schema(input: &NetNodeSchema) -> *const CNetNodeSchema {
    let data = CString::new(input.data.clone()).unwrap();
    let data = data.into_raw();
    let p = CNetNodeSchema {
        id: input.id as u32,
        data,
        is_md: if input.is_md { 1 } else { 0 },
        pos_x: input.pos.x as u32,
        pox_y: input.pos.y as u32,
    };
    Box::into_raw(Box::new(p))
}

pub unsafe fn free_string(s: *mut c_char) {
    if s.is_null() {
        return;
    }
    let _ = CString::from_raw(s);
}

pub unsafe fn copy_net_link_schema(input: &NetLinkSchema) -> *const CNetLinkSchema {
    let p = CNetLinkSchema {
        source: input.source as u32,
        target: input.target as u32,
    };
    Box::into_raw(Box::new(p))
}

pub unsafe fn parse_note_schema(input: *const CNoteSchema) -> NoteSchema {
    let id = (*input).id;
    let name = CStr::from_ptr((*input).name).to_str().unwrap().to_string();
    let url = CStr::from_ptr((*input).url).to_str().unwrap().to_string();
    NoteSchema::new(id as usize, name, url)
}

pub unsafe fn parse_note_schema_vec(input: *const CNoteSchemaVec) -> Vec<NoteSchema> {
    let mut output = Vec::new();
    for i in 0..(*input).len {
        output.push(parse_note_schema(
            (*input).notes.offset(i as isize) as *const CNoteSchema
        ));
    }
    output
}
