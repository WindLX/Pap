import { NoteCreateSchema, NoteRelationshipSchema, NoteUpdateSchema } from "@/schemas/note";
import { TagSetSchema } from "@/schemas/tag";
import { BaseApi } from "./base";
import pFetch from "./fetch";

export class NoteApi extends BaseApi {
    public static async createNote(note: NoteCreateSchema): Promise<NoteRelationshipSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/create_note`, {
                method: "POST",
                body: JSON.stringify(note),
                successMsg: '笔记文件创建成功',
            }).then(async res => {
                const note = await res.json() as NoteRelationshipSchema;
                resolve(note);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async getNotes(): Promise<Array<NoteRelationshipSchema>> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/get_notes`).then(async res => {
                const notes = await res.json() as Array<NoteRelationshipSchema>;
                resolve(notes);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async getNote(noteId: number): Promise<NoteRelationshipSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/get_note?note_id=${noteId}`).then(async res => {
                const note = await res.json() as NoteRelationshipSchema;
                resolve(note);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async getNoteByTags(tagsId: TagSetSchema): Promise<Array<NoteRelationshipSchema>> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/get_note_by_tags`, {
                body: JSON.stringify(tagsId),
            }).then(async res => {
                const notes = await res.json() as Array<NoteRelationshipSchema>;
                resolve(notes);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async getNoteByName(noteName: string): Promise<NoteRelationshipSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/get_note_by_name?note_name=${noteName}`).then(async res => {
                const note = await res.json() as NoteRelationshipSchema;
                resolve(note);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async saveNote(noteId: number, formData: FormData): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/save_note?note_id=${noteId}`, {
                method: 'POST',
                body: formData,
                isForm: true,
                successMsg: '文件保存成功',
            }).then(() => {
                resolve();
            }).catch(err => {
                reject(err);
            })
        })
    }

    public static async renameNote(noteUpdate: NoteUpdateSchema): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/rename_note`, {
                method: 'PUT',
                successMsg: '笔记重命名成功',
                body: JSON.stringify(noteUpdate),
            }).then(() => {
                resolve();
            }).catch(err => {
                reject(err);
            })
        })
    }

    public static async deleteNote(noteId: number): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/delete_note?note_id=${noteId}`, {
                method: 'DELETE',
                successMsg: '笔记文件删除成功',
            }).then(() => {
                resolve();
            }).catch(err => {
                reject(err);
            })
        })
    }

    public static async removeNote(tag_id: number, noteId: number): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/note/remove_note?tag_id=${tag_id}&note_id=${noteId}`, {
                method: 'PUT',
                successMsg: '标签删除成功',
            }).then(() => {
                resolve();
            }).catch(err => {
                reject(err);
            })
        })
    }
}