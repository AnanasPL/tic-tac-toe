import { test, expect } from '@playwright/test';

test.describe('Error Pages', async () => {
  test.describe('Room Not Found', async () => {
    test('should display the correct message', async ({ page }) => {
      await page.goto('/room/aRoomThatDoesNotExist').catch(() => {});
      await page.waitForTimeout(1000); // Requires higher timeout than the one defined in setup.ts. If that ever gets over 1000, then this should be replaced
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