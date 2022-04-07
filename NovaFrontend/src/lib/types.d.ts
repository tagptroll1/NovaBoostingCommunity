/**
 * Can be made globally available by placing this
 * inside `global.d.ts` and removing `export` keyword
 */
export interface Locals {
	code: string;
	userid: string;
}

export interface NovaAccount {
    id?: string;
    account_id: string;
    account_name: string;
    balance?: number;
    wow_characters?: WowCharacter[];
}

export interface WowCharacter {
    character_id: number;
    name: string;
    realm: string;
    faction: string;
    server: string;
    character_class;
    account_id: string;
    paymentcharacter: boolean;
}