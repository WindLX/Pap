import { TagCreateSchema, TagRelationshipSchema, TagSchema } from "@/schemas/tag";
import { BaseApi } from "./base";
import pFetch from "./fetch";
import { NoteRelationshipSchema } from "@/schemas/note";

export class TagApi extends BaseApi {
    public static async createTag(newTag: TagCreateSchema): Promise<TagRelationshipSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/create_tag`, {
                method: "POST",
                body: JSON.stringify(newTag),
                successMsg: '标签创建成功',
            }).then(async res => {
                const tag = await res.json() as TagRelationshipSchema;
                resolve(tag);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async getTags(): Promise<Array<TagRelationshipSchema>> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/get_tags`).then(async res => {
                const tags = await res.json() as Array<TagRelationshipSchema>;
                resolve(tags);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async getNoteTags(noteId: number): Promise<Array<TagRelationshipSchema>> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/get_note_tags?note_id=${noteId}`).then(async res => {
                const tags = await res.json() as Array<TagRelationshipSchema>;
                resolve(tags);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async addTag(tagId: number, noteId: number): Promise<NoteRelationshipSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/add_tag?tag_id=${tagId}&note_id=${noteId}`, {
                method: "PUT",
                successMsg: '标签添加成功',
            }).then(async res => {
                const note = await res.json() as NoteRelationshipSchema;
                resolve(note);
            }).catch(err => {
                reject(err);
            });
        });
    }

    public static async updateTag(newTag: TagSchema): Promise<TagRelationshipSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/update_tag`, {
                method: 'PUT',
                successMsg: '标签更新成功',
                body: JSON.stringify(newTag),
            }).then(async res => {
                const tag = await res.json() as TagRelationshipSchema;
                resolve(tag);
            }).catch(err => {
                reject(err);
            });
        })
    }

    public static async deleteTag(tagId: number): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/delete_tag?tag_id=${tagId}`, {
                method: 'DELETE',
                successMsg: '标签删除成功',
            }).then(() => {
                resolve();
            }).catch(err => {
                reject(err);
            });
        })
    }

    public static async removeTag(tagId: number, noteId: number): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/tag/remove_tag?note_id=${noteId}&tag_id=${tagId}`, {
                method: 'PUT',
                successMsg: '标签移除成功',
            }).then(() => {
                resolve();
            }).catch(err => {
                reject(err);
            });
        })
    }
}