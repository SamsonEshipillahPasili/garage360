from playwright.sync_api import Page, expect


def test_login_page_rejects_invalid_credentials(page: Page):
    page.goto('/accounts/login')
    expect(page.get_by_role('heading', name='Login')).to_be_visible()
    page.locator('#id_username').fill('invalid-username')
    page.locator('#id_password').fill('invalid-password')
    page.get_by_role('button', name='Login').click()

    error = page.locator('.alert.alert-danger')
    expect(error).to_be_visible()
    expect(error).to_contain_text('Please enter a correct username and password. Note that both fields may be case-sensitive.')


