use crate::proto_generator::ProtoGenerator;
use std::{
    ffi::{c_uint, CStr},
    mem::size_of,
};

#[repr(C)]
pub struct CProto {
    data: *const u8,
    len: c_uint,
}

#[repr(C)]
pub struct CProtoVec {
    data: *const *const CProto,
    len: c_uint,
}

#[repr(C)]
pub struct CProtoGenerator {
    content: *mut ProtoGenerator,
}

#[no_mangle]
pub extern "C" fn init_proto_generator(parallel_threshold: c_uint) -> *mut CProtoGenerator {
    let proto_generator = ProtoGenerator::new(parallel_threshold as usize);
    let p = Box::into_raw(Box::new(proto_generator));
    Box::into_raw(Box::new(CProtoGenerator { content: p }))
}

#[no_mangle]
pub unsafe extern "C" fn get_threshold(proto_generator: *mut CProtoGenerator) -> c_uint {
    (*(*proto_generator).content).get_threshold() as c_uint
}

#[no_mangle]
pub unsafe extern "C" fn set_threshold(
    proto_generator: *mut CProtoGenerator,
    parallel_threshold: c_uint,
) {
    (*(*proto_generator).content).set_threshold(parallel_threshold as usize)
}

#[no_mangle]
pub unsafe extern "C" fn generate_proto(
    proto_generator: *mut CProtoGenerator,
    input: *const libc::c_char,
) -> *const CProtoVec {
    let input = CStr::from_ptr(input);
    let input = input.to_str().unwrap().to_string();
    let output = (*(*proto_generator).content).serialize(input);
    let cproto_vec: Vec<*const CProto> = output.iter().map(|o| copy_single_proto(&o)).collect();
    let len = cproto_vec.len();
    let p = libc::malloc(len * size_of::<*const CProto>() as usize);
    std::ptr::copy_nonoverlapping(cproto_vec.as_ptr(), p as *mut *const CProto, len);
    Box::into_raw(Box::new(CProtoVec {
        data: p as *const *const CProto,
        len: len as c_uint,
    }))
}

#[no_mangle]
pub unsafe extern "C" fn free_proto(p: *const CProto) {
    libc::free((*p).data as *mut libc::c_void);
}

#[no_mangle]
pub unsafe extern "C" fn free_proto_vec(p: *const CProtoVec) {
    for p in std::slice::from_raw_parts((*p).data, (*p).len as usize) {
        free_proto(p.clone());
    }
    libc::free((*p).data as *mut libc::c_void);
}

pub unsafe fn copy_single_proto(input: &[u8]) -> *const CProto {
    let len = input.len();
    let p = libc::malloc(len * size_of::<u8>() as usize);
    std::ptr::copy_nonoverlapping(input.as_ptr(), p as *mut u8, len);
    Box::into_raw(Box::new(CProto {
        data: p as *const u8,
        len: len as c_uint,
    }))
}
