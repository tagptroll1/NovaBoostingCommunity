<script lang="ts">
  import type { NovaAccount, WowCharacter } from "$lib/types";
  import {
    DataTable,
    Toolbar,
    ToolbarContent,
    ToolbarSearch,
    Modal,
    Button,
    TextInput,
  } from "carbon-components-svelte";
  import InlineWowCharacter from "./InlineWowCharacter.svelte";

  export let accounts: NovaAccount[] = [];

  let open = false;
  let newAccount: { account_name?: string; account_id?: number } = {
    account_name: null,
    account_id: null,
  };
  let headers = [
    { key: "account_name", value: "Name" },
    { key: "balance", value: "Balance" },
    { key: "account_id", value: "Discord ID" },
  ];
  let rows = accounts.map((a) => ({ ...a, id: a.account_id }));
  const allRows = [...rows];

  function onInput({ target }) {
    const value = target.value.toLowerCase();
    rows = allRows.filter(
      (r) =>
        r.account_name.toLowerCase().includes(value) ||
        r.wow_characters.some(
          (wc) =>
            wc.character_class.toLowerCase() === value ||
            wc.faction.toLowerCase() === value ||
            wc.name.toLowerCase().includes(value) ||
            wc.realm.toLowerCase() === value ||
            wc.server.toLowerCase() === value
        )
    );
  }

  function submit() {
    console.log(newAccount);
  }

  function close() {
    open = false;
    newAccount = { account_name: null, account_id: null };
  }
</script>

<Modal
  size="sm"
  bind:open
  modalHeading="Create Account"
  primaryButtonText="Confirm"
  secondaryButtonText="Cancel"
  on:click:button--secondary={close}
  on:close={close}
  on:submit={submit}
>
  <TextInput bind:value={newAccount.account_name} placeholder="Account Name" />
  <TextInput
    bind:value={newAccount.account_id}
    placeholder="Discord ID (number)"
  />
</Modal>

<DataTable expandable {headers} {rows}>
  <Toolbar>
    <ToolbarContent>
      <ToolbarSearch on:input={onInput} />
      <Button on:click={() => (open = true)}>Create Account</Button>
    </ToolbarContent>
  </Toolbar>
  <div slot="expanded-row" let:row>
    {#each row.wow_characters as character}
      <InlineWowCharacter {character} />
    {/each}
  </div>
</DataTable>

<style>
</style>
