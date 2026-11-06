"""Live-browser acceptance for Moonwake PS-0208 public GitHub Pages release.

The source is private but its static public HTML has the exact same Git blob.
This test exercises user-visible theme persistence, embedded Prompt Library search,
actual clipboard copy, keyboard interaction and mobile layout.
"""
from __future__ import annotations

from playwright.sync_api import sync_playwright, expect

BASE = "https://endeavoreverlasting.github.io/TokenCorridor-prompt-kit-site/"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            permissions=["clipboard-read", "clipboard-write"],
            reduced_motion="reduce",
        )
        page = context.new_page()
        errors = []
        def capture_error(exc):
            errors.append({"message": str(exc), "stack": str(getattr(exc, "stack", ""))[:2500]})
        page.on("pageerror", capture_error)

        page.goto(BASE, wait_until="domcontentloaded", timeout=50000)
        expect(page.get_by_role("heading", name="Moonwake", exact=True)).to_be_visible()
        assert page.locator('img[src="assets/moonwake-mark-512-impeccable.png"]').count() > 0

        selector = page.locator("#appearance")
        selector.select_option("light")
        expect(page.locator("html")).to_have_attribute("data-theme", "light")
        page.reload(wait_until="domcontentloaded")
        expect(page.locator("html")).to_have_attribute("data-theme", "light")
        page.locator("#appearance").select_option("night")
        expect(page.locator("html")).to_have_attribute("data-theme", "night")

        page.locator("#prompts").scroll_into_view_if_needed()
        frame = page.frame_locator("#promptLibraryFrame")
        search = frame.locator("#search")
        search.wait_for(state="visible", timeout=50000)
        search.fill("P04")
        cards = frame.locator(".prompt-card")
        expect(cards.first).to_be_visible(timeout=30000)
        card = cards.first
        card.hover()
        card.locator("button.prompt-copy-btn").click(timeout=15000)
        copied = page.evaluate("navigator.clipboard.readText()")
        assert isinstance(copied, str) and len(copied.strip()) > 60, "copy button did not copy a prompt"

        # Keyboard activation routes to the existing detail; test its Copy control.
        card.focus()
        card.press("Enter")
        detail = frame.locator("#promptDetailOverlay")
        expect(detail).to_have_class(__import__("re").compile(r".*open.*"), timeout=15000)
        frame.locator("#promptDetailCopyTop").click(timeout=15000)
        copied_again = page.evaluate("navigator.clipboard.readText()")
        assert isinstance(copied_again, str) and len(copied_again.strip()) > 60, "detail copy failed"

        direct_href = page.locator("[data-prompt-library]").first.get_attribute("href")
        assert direct_href == "prompt-library/index.html", direct_href

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(BASE, wait_until="domcontentloaded", timeout=50000)
        selector = page.locator("#appearance")
        selector.focus()
        assert selector.evaluate("(el) => document.activeElement === el")
        widths = page.evaluate("({scroll:document.documentElement.scrollWidth, inner:window.innerWidth})")
        if widths["scroll"] > widths["inner"] + 2:
            offenders = page.evaluate("""() => [...document.querySelectorAll('body *')].map(e => {
                const r=e.getBoundingClientRect();
                return {tag:e.tagName.toLowerCase(), id:e.id||'', cls:String(e.className||'').slice(0,70),
                        left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width)}
            }).filter(x=>x.right>innerWidth+2 || x.left<-2).sort((a,b)=>b.right-a.right).slice(0,12)""")
            print("MOBILE_OVERFLOW_ELEMENTS", offenders, flush=True)
        assert widths["scroll"] <= widths["inner"] + 2, widths
        assert not errors, "browser console exceptions: "+repr(errors[:3])
        print("PASS LIVE_BROWSER_MOONWAKE_R3_THEMES_PERSIST_PROMPT_LIBRARY_COPY_KEYBOARD_MOBILE", flush=True)
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
