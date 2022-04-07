<script lang="ts">
    import { NovaApi } from "../api";

    let nova = new NovaApi("http://127.0.0.1:8000/api/v1/");
</script>



{#await nova.get("/accounts/188735535169273858/balance") then response}
{response.amount}
{/await}

{#await nova.get("/accounts?include_balance=true") then response}
{#if response}
{#each response as resp}
    {JSON.stringify(resp)}
{/each}
{/if}
{/await}