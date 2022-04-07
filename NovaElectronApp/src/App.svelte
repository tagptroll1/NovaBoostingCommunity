<script lang="ts">
import AccountBalance from "./Account/AccountBalance.svelte";
import { api } from "./api";

</script>

<header>
	<img src="nova.ico" alt="logo">
	<div class="toolbar-wrapper"></div>
	<div class="window-buttons">
		<button
			id="minibutton"
			on:click="{() => api.send("window::minimize")}">
			—
		</button>
		<button
			id="exitbutton"
			on:click="{() => api.send("window::close")}">
			X
		</button>
	</div>
</header>

<main>
	<AccountBalance></AccountBalance>
</main>

<style lang="scss">
	header {
		width: 100%;
		height: 24px;
		display: flex;
		justify-content: space-between;
		background-color: rgb(71, 71, 71);
		user-select: none;
		
		img {
			pointer-events: none;
			height: 100%;
			width: auto;
		}
		
		.toolbar-wrapper {
			-webkit-app-region: drag;
			flex-grow: 1;
		}

		.window-buttons {
			display: flex;
			button {
				padding: 0;
				margin: 0;
				height: 100%;
				width: 25px;
				border: none;
				border-radius: 0;
				color: lightgrey;
				background-color: rgb(71, 71, 71);
				
				&:hover {
					background-color: rgb(114, 114, 114);
				}
				+ #exitbutton:hover {
					background-color: rgb(167, 50, 50);
				}
			}
		}
	}
</style>