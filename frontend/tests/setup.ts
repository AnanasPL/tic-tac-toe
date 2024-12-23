import { BrowserContext } from '@playwright/test';

const setUpAllPages = async (context: BrowserContext, count: number = 2) => {
  for (let i = 0; i < count; i++) {
    await (await context.newPage()).goto('/');
  }
};

const createANewRoomAndJoinIt = async (context: BrowserContext) => {
  const [page1, page2] = context.pages();

  await page1.getByText('Create New Room').click();
  await page2.getByText(/^[a-zA-z0-9]{6}1\/2$/).click();
};

const playTheGame = async (context: BrowserContext) => {
  const [page1, page2] = context.pages();

  await page1.locator('.cell').nth(0).click();
  await page2.locator('.cell').nth(3).click();
  await page1.locator('.cell').nth(1).click();
  await page2.locator('.cell').nth(4).click();
  await page1.locator('.cell').nth(2).click();
  await page1.waitForTimeout(500);
};

const restartTheGame = async (context: BrowserContext) => {
  const [page1, page2] = context.pages();

  await page1.locator('.buttons button').first().click();
  await page2.locator('.buttons button').first().click();
};

export { setUpAllPages, createANewRoomAndJoinIt, playTheGame, restartTheGame };