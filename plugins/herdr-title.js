export const HerdrTitlePlugin = async ({ $ }) => ({
  event: async ({ event }) => {
    if (!process.env.HC_TERMINAL_ID || event.type !== "session.updated") return;
    const title = event.properties?.info?.title?.trim();
    if (!title) return;
    await $`python3 /Users/ym/Dev/ai-root/scripts/herdr-auto-title.py --set ${title}`.quiet().nothrow();
  },
});
