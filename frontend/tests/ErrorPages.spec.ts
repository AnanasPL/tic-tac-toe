import { test, expect } from '@playwright/test';

test.describe('Error Pages', async () => {
  test.describe('Room Not Found', async () => {
    test('should display the correct message', async ({ page }) => {
      await page.goto('/room/aRoomThatDoesNotExist').catch(() => {});
      await page.waitForTimeout(1000);
      await expect(page.url().endsWith('room-not-found')).toBeTruthy();
      await expect(page.locator('.error-message')).toHaveText('There is no room with the code: aRoomThatDoesNotExist');
    });
  });

  test.describe('Page Not Found', async () => {
    test('should display the correct message', async ({ page }) => {
      await page.goto('/aPageThatCertainlyDoesNotExist');

      await expect(page.locator('.error-message')).toHaveText('Page was not found');
    })
  })
});