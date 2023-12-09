use std::{
    fmt::Debug,
    ops::{Index, IndexMut, Range},
};

#[derive(Clone)]
pub struct MdChars {
    length: usize,
    data: *const [u8],
}

impl Debug for MdChars {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let data_slice: &[u8] = unsafe { &*self.data };
        write!(
            f,
            "MdChars {{ length: {}, data: {:#?} }}",
            self.length,
            std::str::from_utf8(data_slice).unwrap()
        )
    }
}

unsafe impl Sync for MdChars {}

impl ToString for MdChars {
    fn to_string(&self) -> String {
        let s: &str = (*self).clone().into();
        s.to_string()
    }
}

#[derive(Debug, Clone)]
pub struct MdCharsIter {
    offset: usize,
    data: MdChars,
}

impl MdChars {
    pub fn new(data: &[u8]) -> Self {
        Self {
            length: data.len(),
            data: &*data as *const [u8],
        }
    }

    pub fn len(&self) -> usize {
        self.length
    }

    pub fn is_empty(&self) -> bool {
        self.length == 0
    }

    pub fn as_bytes(&self) -> &[u8] {
        <MdChars as Into<&[u8]>>::into(self.clone())
    }
}

impl MdCharsIter {
    pub fn is_end(&self) -> bool {
        self.offset + 1 >= self.data.len()
    }

    pub fn peek(&self) -> u8 {
        if self.data.len() == self.offset {
            return 0;
        }
        self.data[self.offset]
    }

    pub fn check(&self, target: u8) -> bool {
        self.peek() == target
    }

    pub fn check_multi(&self, target: &[u8]) -> bool {
        let mut result = true;
        if self.offset + target.len() > self.data.len() {
            return false;
        }
        for i in 0..target.len() {
            result &= self.data[self.offset + i] == target[i];
        }
        result
    }

    pub fn check_str(&self, target: &str) -> bool {
        self.check_multi(target.as_bytes())
    }

    pub fn slice_to_byte(&mut self, end: u8) -> &[u8] {
        let start = self.offset;
        loop {
            if self.check(end) {
                self.offset += 1;
                return &self.data[start..self.offset - 1];
            } else {
                if self.offset + 1 < self.data.len() {
                    self.offset += 1;
                } else {
                    return &self.data[start..self.data.len()];
                }
            }
        }
    }

    pub fn slice_to_array(&mut self, end: &[u8]) -> &[u8] {
        let start = self.offset;
        loop {
            if self.check_multi(end) {
                self.offset += end.len();
                return &self.data[start..self.offset - end.len()];
            } else {
                if self.offset + end.len() < self.data.len() {
                    self.offset += 1;
                } else {
                    self.offset = self.data.len();
                    return &self.data[start..self.data.len()];
                }
            }
        }
    }

    pub fn slice_to_array_2(&mut self, end: &[u8], short_end: &[u8]) -> &[u8] {
        let start = self.offset;
        loop {
            if self.check_multi(end) {
                self.offset += end.len();
                return &self.data[start..self.offset - end.len()];
            } else if self.check_multi(short_end) {
                self.offset += short_end.len();
                return &self.data[start..self.offset - short_end.len()];
            } else {
                if self.offset + end.len() < self.data.len() {
                    self.offset += 1;
                } else {
                    self.offset = self.data.len();
                    return &self.data[start..self.data.len()];
                }
            }
        }
    }

    pub fn slice_to_str_2(&mut self, end: &str, short_end: &str) -> &[u8] {
        let end = end.as_bytes();
        let short_end = short_end.as_bytes();
        self.slice_to_array_2(end, short_end)
    }

    pub fn slice_to_str(&mut self, end: &str) -> &[u8] {
        let end = end.as_bytes();
        self.slice_to_array(end)
    }
}

impl Index<usize> for MdChars {
    type Output = u8;
    fn index(&self, index: usize) -> &Self::Output {
        if index < self.length {
            unsafe { &(*self.data)[index] }
        } else {
            panic!(
                "Index out of range: length is {}, and index is {}",
                self.length, index
            )
        }
    }
}

impl Index<Range<usize>> for MdChars {
    type Output = [u8];
    fn index(&self, range: Range<usize>) -> &Self::Output {
        unsafe { &(*self.data)[range.start..range.end] }
    }
}

impl IndexMut<usize> for MdChars {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        if index < self.length {
            unsafe { &mut (*self.data.cast_mut())[index] }
        } else {
            panic!("Index out of range")
        }
    }
}

impl IntoIterator for MdChars {
    type Item = u8;
    type IntoIter = MdCharsIter;
    fn into_iter(self) -> Self::IntoIter {
        MdCharsIter {
            offset: 0,
            data: self,
        }
    }
}

impl From<&str> for MdChars {
    fn from(value: &str) -> Self {
        Self::new(value.as_bytes())
    }
}

impl<'a> Into<&'a str> for MdChars {
    fn into(self) -> &'a str {
        unsafe { std::str::from_utf8(self.data.as_ref().unwrap()).unwrap() }
    }
}

impl<'a> Into<&'a [u8]> for MdChars {
    fn into(self) -> &'a [u8] {
        unsafe { std::slice::from_raw_parts(self.data as *const u8, self.length) }
    }
}

impl Iterator for MdCharsIter {
    type Item = u8;
    fn next(&mut self) -> Option<Self::Item> {
        if self.offset < self.data.length {
            let item = (self.data)[self.offset];
            self.offset += 1;
            Some(item)
        } else {
            None
        }
    }
}

impl From<&[u8]> for MdCharsIter {
    fn from(value: &[u8]) -> Self {
        MdChars::new(value).into_iter()
    }
}

#[cfg(test)]
mod test_chars {
    use super::MdChars;

    #[test]
    fn test_index() {
        let chars = MdChars::new(&mut [1, 2, 3, 4, 5]);
        for i in 0..5 {
            assert_eq!(chars[i] - 1, i as u8)
        }
    }

    #[test]
    fn test_index_mut() {
        let mut chars = MdChars::new(&mut [1, 2, 3, 4, 5]);
        chars[0] = 10;
        assert_eq!(chars[0], 10);
        for i in 1..5 {
            assert_eq!(chars[i] - 1, i as u8)
        }
    }

    #[test]
    fn test_from() {
        let chars = MdChars::from("12345");
        for i in 0..5 {
            assert_eq!(chars[i] - b'0', i as u8 + 1)
        }
    }

    #[test]
    fn test_into() {
        let chars = MdChars::from("测试");
        assert_eq!(<MdChars as Into<&str>>::into(chars), "测试")
    }

    #[test]
    fn test_len() {
        let chars = MdChars::from("测试");
        assert_eq!(chars.len(), 6)
    }

    #[test]
    fn test_empty() {
        let chars = MdChars::new(&[]);
        assert_eq!(chars.is_empty(), true);
        let chars = MdChars::new(&[1]);
        assert_eq!(chars.is_empty(), false);
    }
}

#[cfg(test)]
mod test_chars_iter {
    use super::MdChars;

    const CHARS: &[u8] = &[1, 2, 3, 4, 5];

    #[test]
    fn test_peek() {
        let chars = MdChars::new(CHARS);
        assert_eq!(chars.into_iter().peek(), 1)
    }

    #[test]
    fn test_next() {
        let chars = MdChars::new(CHARS);
        let mut chars_iter = chars.into_iter();
        for i in 0..5 {
            assert_eq!(chars_iter.next(), Some(i + 1));
        }
    }

    #[test]
    fn test_check() {
        let chars = MdChars::new(CHARS);
        assert_eq!(chars.into_iter().check(b'1' - b'0'), true);
    }

    #[test]
    fn test_check_multi() {
        let chars = MdChars::new(CHARS);
        assert_eq!(
            chars
                .clone()
                .into_iter()
                .check_multi(&[b'1' - b'0', b'2' - b'0']),
            true
        );
        assert_ne!(
            chars.into_iter().check_multi(&[
                b'1' - b'0',
                b'2' - b'0',
                b'3' - b'0',
                b'4' - b'0',
                b'5' - b'0',
                b'6' - b'0'
            ]),
            true
        );
    }

    #[test]
    fn test_slice() {
        let mut chars = MdChars::from("123\n456\n789").into_iter();
        assert_eq!(chars.slice_to_byte(b'\n'), &[b'1', b'2', b'3']);
        assert_eq!(chars.slice_to_byte(b'\n'), &[b'4', b'5', b'6']);
        assert_eq!(chars.slice_to_byte(b'\n'), &[b'7', b'8', b'9']);
        assert_eq!(chars.is_end(), true);
    }

    #[test]
    fn test_slice_multi() {
        let mut chars = MdChars::from("$$123\n$$789\n").into_iter();
        chars.slice_to_array(&[b'$', b'$']);
        assert_eq!(
            chars.slice_to_array(&[b'$', b'$']),
            &[b'1', b'2', b'3', b'\n']
        );
        assert_eq!(
            chars.slice_to_array(&[b'$', b'$']),
            &[b'7', b'8', b'9', b'\n']
        );
    }

    #[test]
    fn test_slice_by_str() {
        let mut chars = MdChars::from("$$123\n$$789\n000").into_iter();
        chars.slice_to_str("$$");
        assert_eq!(chars.slice_to_str("$$"), &[b'1', b'2', b'3', b'\n']);
        assert_eq!(
            chars.slice_to_str("$$"),
            &[b'7', b'8', b'9', b'\n', b'0', b'0', b'0']
        );
    }
}
