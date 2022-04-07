<script context="module" lang="ts">

	export function load({session, page}) {
		if (session?.loggedIn) {
			return {status: 200}
		}
		return { status: 404, error: new Error(`NotFound: ${page.path}`) }
	}
</script>

<slot></slot>