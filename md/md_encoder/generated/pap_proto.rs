#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Block {
    #[prost(oneof = "block::Block", tags = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11")]
    pub block: ::core::option::Option<block::Block>,
}
/// Nested message and enum types in `Block`.
pub mod block {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Block {
        #[prost(message, tag = "1")]
        Title(super::Title),
        #[prost(message, tag = "2")]
        Paragraph(super::Paragraph),
        #[prost(message, tag = "3")]
        Quote(super::Quote),
        #[prost(message, tag = "4")]
        ListItem(super::ListItem),
        #[prost(message, tag = "5")]
        CodeBlock(super::CodeBlock),
        #[prost(message, tag = "6")]
        Image(super::Image),
        #[prost(message, tag = "7")]
        Line(super::Line),
        #[prost(message, tag = "8")]
        MathBlock(super::MathBlock),
        #[prost(message, tag = "9")]
        TableBlock(super::TableBlock),
        #[prost(message, tag = "10")]
        TodoItem(super::TodoItem),
        #[prost(message, tag = "11")]
        Footer(super::Footer),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Title {
    #[prost(enumeration = "title::TitleLevel", tag = "1")]
    pub level: i32,
    #[prost(message, optional, tag = "2")]
    pub content: ::core::option::Option<Paragraph>,
}
/// Nested message and enum types in `Title`.
pub mod title {
    #[derive(
        Clone,
        Copy,
        Debug,
        PartialEq,
        Eq,
        Hash,
        PartialOrd,
        Ord,
        ::prost::Enumeration
    )]
    #[repr(i32)]
    pub enum TitleLevel {
        H1 = 0,
        H2 = 1,
        H3 = 2,
        H4 = 3,
        H5 = 4,
        H6 = 5,
    }
    impl TitleLevel {
        /// String value of the enum field names used in the ProtoBuf definition.
        ///
        /// The values are not transformed in any way and thus are considered stable
        /// (if the ProtoBuf definition does not change) and safe for programmatic use.
        pub fn as_str_name(&self) -> &'static str {
            match self {
                TitleLevel::H1 => "H1",
                TitleLevel::H2 => "H2",
                TitleLevel::H3 => "H3",
                TitleLevel::H4 => "H4",
                TitleLevel::H5 => "H5",
                TitleLevel::H6 => "H6",
            }
        }
        /// Creates an enum from field names used in the ProtoBuf definition.
        pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
            match value {
                "H1" => Some(Self::H1),
                "H2" => Some(Self::H2),
                "H3" => Some(Self::H3),
                "H4" => Some(Self::H4),
                "H5" => Some(Self::H5),
                "H6" => Some(Self::H6),
                _ => None,
            }
        }
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Paragraph {
    #[prost(message, repeated, tag = "1")]
    pub sentences: ::prost::alloc::vec::Vec<Sentence>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Quote {
    #[prost(message, repeated, tag = "1")]
    pub sentences: ::prost::alloc::vec::Vec<Sentence>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ListItem {
    #[prost(uint32, tag = "1")]
    pub level: u32,
    #[prost(uint32, optional, tag = "2")]
    pub index: ::core::option::Option<u32>,
    #[prost(message, optional, tag = "3")]
    pub content: ::core::option::Option<Paragraph>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CodeBlock {
    #[prost(string, optional, tag = "1")]
    pub language: ::core::option::Option<::prost::alloc::string::String>,
    #[prost(string, tag = "2")]
    pub code: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Image {
    #[prost(string, optional, tag = "1")]
    pub title: ::core::option::Option<::prost::alloc::string::String>,
    #[prost(string, optional, tag = "2")]
    pub src: ::core::option::Option<::prost::alloc::string::String>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Line {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MathBlock {
    #[prost(string, tag = "1")]
    pub math: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TableBlock {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TodoItem {
    #[prost(bool, tag = "1")]
    pub is_finished: bool,
    #[prost(message, optional, tag = "2")]
    pub content: ::core::option::Option<Paragraph>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Footer {
    #[prost(message, optional, tag = "1")]
    pub index: ::core::option::Option<FooterIndex>,
    #[prost(message, optional, tag = "2")]
    pub content: ::core::option::Option<Paragraph>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Sentence {
    #[prost(oneof = "sentence::Sentence", tags = "1, 2, 3, 4, 5, 6")]
    pub sentence: ::core::option::Option<sentence::Sentence>,
}
/// Nested message and enum types in `Sentence`.
pub mod sentence {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Sentence {
        #[prost(message, tag = "1")]
        Text(super::Text),
        #[prost(message, tag = "2")]
        Link(super::Link),
        #[prost(string, tag = "3")]
        Code(::prost::alloc::string::String),
        #[prost(string, tag = "4")]
        Math(::prost::alloc::string::String),
        #[prost(string, tag = "5")]
        Emoji(::prost::alloc::string::String),
        #[prost(message, tag = "6")]
        FooterIndex(super::FooterIndex),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FooterIndex {
    #[prost(string, tag = "1")]
    pub index: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Text {
    #[prost(string, tag = "1")]
    pub content: ::prost::alloc::string::String,
    #[prost(bool, tag = "2")]
    pub is_bold: bool,
    #[prost(bool, tag = "3")]
    pub is_italic: bool,
    #[prost(bool, tag = "4")]
    pub is_strike: bool,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Link {
    #[prost(string, tag = "1")]
    pub content: ::prost::alloc::string::String,
    #[prost(string, optional, tag = "2")]
    pub href: ::core::option::Option<::prost::alloc::string::String>,
}
