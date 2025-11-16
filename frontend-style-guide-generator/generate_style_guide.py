import argparse
import cssutils
from collections import Counter
from playwright.sync_api import sync_playwright

def generate_style_guide(url):
    """
    Analyzes a web page's CSS to find common colors, fonts, and spacing,
    and then generates a STYLE_GUIDE.md document.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            # Find all stylesheet links
            stylesheet_links = page.eval_on_selector_all('link[rel="stylesheet"]', 'elements => elements.map(e => e.href)')

            # Get inline styles
            inline_styles = page.eval_on_selector_all('[style]', 'elements => elements.map(e => e.getAttribute("style"))')

            all_css_text = "\n".join(inline_styles)

            # Fetch and combine all external stylesheets
            for link in stylesheet_links:
                try:
                    style_tag = page.query_selector(f'link[href="{link}"]')
                    if style_tag:
                         all_css_text += page.evaluate('(element) => { return element.sheet.cssText; }', style_tag)
                except Exception:
                    # The above might fail due to CORS or other issues.
                    # As a fallback, try to fetch the content directly.
                    try:
                         response = page.request.get(link)
                         if response.ok:
                              all_css_text += response.text()
                    except Exception as e:
                         print(f"Could not fetch stylesheet at {link}: {e}")

            browser.close()

        # Parse the CSS with cssutils
        parser = cssutils.CSSParser()
        sheet = parser.parseString(all_css_text)

        colors = Counter()
        font_families = Counter()
        font_sizes = Counter()
        spacings = Counter()

        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for prop in rule.style:
                    if 'color' in prop.name.lower():
                        colors[prop.value] += 1
                    elif 'font-family' in prop.name.lower():
                        font_families[prop.value] += 1
                    elif 'font-size' in prop.name.lower():
                        font_sizes[prop.value] += 1
                    elif prop.name.lower() in ['margin', 'padding', 'gap']:
                        spacings[prop.value] += 1

        # Generate the STYLE_GUIDE.md
        with open('STYLE_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write("# Frontend Style Guide\n\n")
            f.write("## Colors\n")
            for color, count in colors.most_common(10):
                f.write(f"- `{color}` (used {count} times)\n")

            f.write("\n## Font Families\n")
            for font, count in font_families.most_common(5):
                f.write(f"- `{font}` (used {count} times)\n")

            f.write("\n## Font Sizes\n")
            for size, count in font_sizes.most_common(5):
                f.write(f"- `{size}` (used {count} times)\n")

            f.write("\n## Spacing Units\n")
            for space, count in spacings.most_common(5):
                f.write(f"- `{space}` (used {count} times)\n")

        print("STYLE_GUIDE.md generated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have run 'playwright install' to install the necessary browsers.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a frontend style guide from a URL.")
    parser.add_argument("url", help="The URL of the website to analyze.")
    args = parser.parse_args()
    generate_style_guide(args.url)
