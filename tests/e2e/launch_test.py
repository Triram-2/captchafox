import pytest
from captchafox import Captchafox


@pytest.mark.asyncio
async def test_launch_without_headless() -> None:
    async with Captchafox(headless=True) as browser:
        page = await browser.new_page()
        await page.goto("https://www.whatismybrowser.com/detect/what-are-my-browsers-navigator-properties/")
        title = await page.title()
        assert "What are my browser's navigator properties?" in title


@pytest.mark.asyncio
async def test_launch_with_headless() -> None:
    async with Captchafox(headless=True) as browser:
        page = await browser.new_page()
        await page.goto("https://www.whatismybrowser.com/detect/what-are-my-browsers-navigator-properties/")
        title = await page.title()
        assert "What are my browser's navigator properties?" in title
