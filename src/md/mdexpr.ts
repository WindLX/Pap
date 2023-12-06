export interface Block {
    tag: BlockTag,
    content: Title | Paragraph | ListItem
    | [string, string] | Image | string
    | TodoItem | Footer | undefined
}

export enum BlockTag {
    Title = "Title",
    Paragraph = "Paragraph",
    Quote = "Quote",
    ListItem = "ListItem",
    CodeBlock = "CodeBlock",
    Image = "Image",
    Line = "Line",
    MathBlock = "MathBlock",
    TodoItem = "TodoItem",
    Footer = "Footer",
    Error = "Error"
}

export interface Title {
    level: TitleLevel,
    content: Paragraph,
}

export interface RawTitle {
    line: number,
    level: TitleLevel,
    content: string,
}

export enum TitleLevel {
    H1 = "H1",
    H2 = "H2",
    H3 = "H3",
    H4 = "H4",
    H5 = "H5",
    H6 = "H6"
}

export type Paragraph = Array<Sentence>

export interface Sentence {
    tag: SentenceTag,
    content: Text | Link | string | FooterIndex
}

export enum SentenceTag {
    Text = "Text",
    Link = "Link",
    Code = "Code",
    Math = "Math",
    Emoji = "Emoji",
    FooterIndex = "FooterIndex"
}

export interface Text {
    content: string,
    is_bold: boolean,
    is_italic: boolean,
    is_strike: boolean,
}

export interface Link {
    content: string,
    href: string | undefined
}

export interface ListItem {
    level: number,
    index: number | undefined,
    content: Paragraph,
}

export interface Image {
    title: string | undefined,
    src: string | undefined,
}

export interface TodoItem {
    is_finished: boolean,
    content: Paragraph
}

export interface Footer {
    index: FooterIndex,
    content: Paragraph
}

export type FooterIndex = string