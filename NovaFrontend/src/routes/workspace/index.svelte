<script context="module" lang="ts">
	export async function load({session, fetch}) {
        const response = await fetch("api/accounts");
        
        if (response.ok) {
            const accounts = await response.json();
            return {props: {accounts}}
        }  else {
            return {status: 400}
        }
	}
</script>

<script lang="ts">
    import type { NovaAccount } from "$lib/types";
    import AccountList from "$lib/workspace/AccountList.svelte";

    export let accounts: NovaAccount[];
</script>

<h1>Welcome to your workspace</h1>

<AccountList {accounts} />


<style>
    h1 {
        margin-bottom: 50px;
    }
</style>