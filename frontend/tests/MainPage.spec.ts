import { test, expect } from '@playwright/test';
import { setUpAllPages, TIMEOUT } from './setup';

test.describe('Main Page', async () => {
  test.beforeEach(async ({ context }) => setUpAllPages(context, 3));
  
  test('should have correct title', async ({ context }) => {
    const [page1] = context.pages();

    await expect(page1).toHaveTitle('Tic Tac Toe');
  });
  
  test.describe('Creating/Removing rooms', async () => {
    test('should display the Create New Room button', async ({ context }) => {
      const [page1] = context.pages();

      await expect(page1.locator('.add-room-button')).toBeVisible();
    });
    
    // This test may sometimes give wrong output and always be true, as there is no way to clear all the rooms manually,
    // but since the next test checks if the code of the new room is different than the previous one, it's safe to assume
    // that the output this test is actually true, when the other passes. Though, might be useful in the future
    test('should add a new room when clicked', async ({ context }) => {
      const [page1, page2] = context.pages();
      
      await page1.locator('.add-room-button').click();
      await page2.waitForTimeout(TIMEOUT);

      await expect(page2.locator('.room')).toBeVisible();
    });
    
    test('should remove empty room and make a new one', async ({ context }) => {
      const [page1, page2] = context.pages();

      await page1.locator('.add-room-button').click();
      await page2.waitForTimeout(TIMEOUT);

      const oldCode = (await page2.locator('.room').textContent())?.substring(0, 6);
      
      await page1.waitForTimeout(TIMEOUT);
      await page1.goto('/');

      await page1.locator('.add-room-button').click();
      await page2.waitForTimeout(TIMEOUT);
      
      const newCode = (await page2.locator('.room').textContent())?.substring(0, 6);

      await expect(oldCode).not.toBe(newCode);
    });
  });
  
  test.describe('Joining rooms', async () => {
    test('should redirect to the room page when the room is clicked', async ({ context }) => {
      const [page1, page2] = context.pages();
      
      await page1.locator('.add-room-button').click();

      await page2.waitForTimeout(TIMEOUT);
      const roomCode = (await page2.locator('.room').textContent())?.substring(0, 6);
      await page2.locator('.room').click();
      await page2.waitForTimeout(TIMEOUT);
      
      await expect(page2.url().endsWith(roomCode!)).toBeTruthy();
    });
    
    test('should not redirect to the room page when the room is full', async ({ context }) => {
      const [page1, page2, page3] = context.pages();
      
      await page1.locator('.add-room-button').click();
      await page2.waitForTimeout(TIMEOUT);
      await page2.locator('.room').click();
      await page3.waitForTimeout(TIMEOUT);
      await page3.locator('.room').click();
      
      await page3.waitForTimeout(TIMEOUT);
      // Having URL checked this way makes it not hardcoded into the tests, so if it ever 
      // changes, the only url that needs to be changed is in frontend/playwright.config.ts
      await expect(page3).toHaveURL(page2.url().split('room')[0]);
    });
    
    test('should display correct number of players inside the room', async ({ context }) => {
      const [page1, page2, page3] = context.pages();
  
      await page1.locator('.add-room-button').click();    
      await page1.waitForTimeout(TIMEOUT);
      await page1.goto('/');
      
      const room1 = await page1.locator('.room');
      await expect(room1).toHaveText(/^[a-zA-z0-9]{6}0\/2$/);
      await room1.click();
  
      const room2 = await page2.locator('.room');
      await expect(room2).toHaveText(/^[a-zA-z0-9]{6}1\/2$/);
      await room2.click();
      
      await expect(page3.locator('.room')).toHaveText(/^[a-zA-z0-9]{6}2\/2$/);
    });
  });
});