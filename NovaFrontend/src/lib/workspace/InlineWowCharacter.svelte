<script lang="ts">
import type { WowCharacter } from "$lib/types";


    export let character: WowCharacter;
</script>

<span class="character {character.character_class.replace(" ", "-")}">
    {character.name}-{character.realm} [{character.faction === "horde" ? "H": "A"}]
</span>

<style>
    .character {
        display: inline-flex;
        align-items: center;
        justify-content: center;

        margin-right: 5px;
        padding: 3px;
        border-radius: 3px;
        border: 1px solid black;
        color: white;
        text-shadow: black 0 0 2px,
                    black 1px 1px 2px,
                    black -1px -1px 2px;
    }
</style>