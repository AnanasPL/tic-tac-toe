import { test, expect, Page } from '@playwright/test';
import { 
  setUpAllPages, 
  createANewRoomAndJoinIt, 
  playTheGame, 
  restartTheGame, 
  TIMEOUT
} from './setup';

const MESSAGES = [
  'Wait for the other player',
  'Wait for your turn',
  'This field is already taken'
];

test.describe('Game Page', async () => {
  test.beforeEach(async ({ context }) => {
    await setUpAllPages(context);
    await createANewRoomAndJoinIt(context);
  });

  test.describe('Go Back Button', async () => {
    test('should display the Go Back button', async ({ context }) => {
      const [page1] = context.pages();

      await expect(page1.locator('.go-back-button')).toBeVisible();
    });

    test('should redirect to the main page when clicked', async ({ context }) => {
      const [page1, page2] = context.pages();

      await page1.locator('.go-back-button').click();

      await expect(page1).toHaveURL(page2.url().split('room')[0]);
    });
  });
  
  test.describe('Bottom Message', async () => {
    test('should display empty message at the start', async ({ context }) => {
      const [page1] = context.pages();

      await expect(page1.locator('.message')).toHaveText('');
    });

    test('should display the correct message when there is only one player', async ({ context }) => {
      const [page1, page2] = context.pages();

      await page2.goto('/');
      await page1.locator('.cell').nth(0).click();

      await expect(page1.locator('.message')).toHaveText(MESSAGES[0]);
    });

    // Multiple expect statements are to ensure the turn is changed properly
    test('should display the correct message when the wrong player makes a move', async ({ context }) => {
      const [page1, page2] = context.pages();

      await page2.locator('.cell').nth(0).click();

      await expect(page2.locator('.message')).toHaveText(MESSAGES[1]);

      await page1.locator('.cell').nth(0).click();
      await page1.locator('.cell').nth(1).click();

      await expect(page1.locator('.message')).toHaveText(MESSAGES[1]);
    });

    test('should display the correct message when the player clicks on the field that is already taken', async ({ context }) => {
      const [page1, page2] = context.pages();

      await page1.locator('.cell').nth(0).click();
      await page2.locator('.cell').nth(0).click();

      await expect(page2.locator('.message')).toHaveText(MESSAGES[2]);
    });

    test('should clear the message when correct move is made', async ({ context }) => {
      const [page1, page2] = context.pages();

      await page1.locator('.cell').nth(0).click();
      await page2.locator('.cell').nth(0).click();
      
      // Making sure the field actually changes
      await expect(page2.locator('.message')).not.toHaveText('');

      await page2.locator('.cell').nth(1).click();

      await expect(page2.locator('.message')).toHaveText('');
    });  
  });

  test.describe('Board', async () => {
    test.describe('Displaying', async () => {
      test('should display the board', async ({ context }) => {
        const [page1] = context.pages();

        await expect(page1.locator('.board')).toBeVisible();
      });    

      test('should display the lines', async ({ context }) => {
        const [page1] = context.pages();
  
        for (const line of await page1.locator('.line').all()) {
          await expect(line).toBeVisible();
        }
  
        await expect((await page1.locator('.line').all()).length).toBe(4);
      });
  
      test('should display the cells', async ({ context }) => {
        const [page1] = context.pages();
  
        for (const cell of await page1.locator('.cell').all()) {
          await expect(cell).toBeVisible();
        }
  
        await expect((await page1.locator('.cell').all()).length).toBe(9);
      });
  
      test('should have empty text in each cell at the start', async ({ context }) => {
        const [page1] = context.pages();
  
        for (const cell of await page1.locator('.cell').all()) {
          await expect(cell).toHaveText('');
        }
      });
  
      test('should change the cell text when clicked', async ({ context }) => {
        const [page1, page2] = context.pages();
  
        await page1.locator('.cell').nth(0).click();
        await page2.locator('.cell').nth(1).click();
  
        await expect(page1.locator('.cell').nth(0)).toHaveText(/^[OX]$/);
        await expect(page2.locator('.cell').nth(1)).toHaveText(/^[OX]$/);
      });
    });
    
    test.describe('Playing the game', async () => {     
      test('should change the cell when the correct player clicked', async ({ context }) => {
        const [page1, page2] = context.pages();

        await page1.locator('.cell').nth(0).click();

        await expect(page1.locator('.cell').nth(0)).toHaveText('O');
        await expect(page2.locator('.cell').nth(0)).toHaveText('O');
        
        await page2.locator('.cell').nth(1).click();

        await expect(page1.locator('.cell').nth(1)).toHaveText('X');
        await expect(page2.locator('.cell').nth(1)).toHaveText('X');
      });

      test('should not change the cell when the wrong player clicked', async ({ context }) => {
        const [page1, page2] = context.pages();

        await page2.locator('.cell').nth(0).click();

        await expect(page1.locator('.cell').nth(0)).toHaveText('');
        await expect(page2.locator('.cell').nth(0)).toHaveText('');
        
        await page1.locator('.cell').nth(0).click();
        await page1.locator('.cell').nth(1).click();

        await expect(page1.locator('.cell').nth(1)).toHaveText('');
        await expect(page2.locator('.cell').nth(1)).toHaveText('');
      });

      test.describe('Rejoining', async () => {
        test('should not mess up the turn', async ({ context }) => {
          const [page1, page2] = context.pages();
          
          await rejoin(page2);
          await page2.locator('.cell').first().click();
          await expect(page2.locator('.cell').first()).toHaveText('');

          await rejoin(page1)
          await page1.locator('.cell').first().click();
          await expect(page1.locator('.cell').first()).not.toHaveText('');

          await page2.locator('.cell').nth(2).click();
          await expect(page2.locator('.cell').nth(2)).not.toHaveText('');
        });

        // This test is EXTREMELY buggy, almost always gives different results on non-chromium clients 
        // (especially webkit). It seems like the problem lies in playwright, since manual tests and deep
        // inspection confirmed that the functionality works as expected (not tested on webkit yet).
        test('should not mess up the symbols', async ({ context }) => {
          const [page1, page2] = context.pages();

          await rejoin(page1);
          await page1.locator('.cell').first().click();

          await expect(page1.locator('.cell').first()).toHaveText('O');

          await rejoin(page2);
          await page2.locator('.cell').nth(2).click();

          await expect(page2.locator('.cell').nth(2)).toHaveText('X');
        });

        test('should show the play popup after rejoin', async ({ context }) => {
          await playTheGame(context); 
          const [page1] = context.pages();

          await page1.goto('/');
          await page1.locator('.room').click();

          await expect(page1.locator('.overlay')).toBeVisible();
        });
      });
    });
  });
  
  test.describe('After The Game', async () => {
    test.describe('should display the popup after the game ends', async () => {
      test('first player won', async ({ context }) => {
        const [page1, page2] = context.pages();
  
        await page1.locator('.cell').nth(0).click();
        await page2.locator('.cell').nth(3).click();
        await page1.locator('.cell').nth(1).click();
        await page2.locator('.cell').nth(4).click();
        await page1.locator('.cell').nth(2).click();
  
        await expect(page1.locator('.overlay')).toBeVisible();
        await expect(page2.locator('.overlay')).toBeVisible();
      });
  
      test('second player won', async ({ context }) => {
        const [page1, page2] = context.pages();
  
        await page1.locator('.cell').nth(0).click();
        await page2.locator('.cell').nth(3).click();
        await page1.locator('.cell').nth(1).click();
        await page2.locator('.cell').nth(4).click();
        await page1.locator('.cell').nth(6).click();
        await page2.locator('.cell').nth(5).click();
  
        await expect(page1.locator('.overlay')).toBeVisible();
        await expect(page2.locator('.overlay')).toBeVisible();
      });
  
      test('tie', async ({ context }) => {
        const [page1, page2] = context.pages();
  
        await page1.locator('.cell').nth(0).click();
        await page2.locator('.cell').nth(8).click();
        await page1.locator('.cell').nth(1).click();
        await page2.locator('.cell').nth(7).click();
        await page1.locator('.cell').nth(6).click();
        await page2.locator('.cell').nth(2).click();
        await page1.locator('.cell').nth(5).click();
        await page2.locator('.cell').nth(3).click();
        await page1.locator('.cell').nth(4).click();
  
        await expect(page1.locator('.overlay')).toBeVisible();
        await expect(page2.locator('.overlay')).toBeVisible();
      });

      test.describe('Showing the winner correctly', async () => {
        test('first player won', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page1.locator('.cell').nth(0).click();
          await page2.locator('.cell').nth(3).click();
          await page1.locator('.cell').nth(1).click();
          await page2.locator('.cell').nth(4).click();
          await page1.locator('.cell').nth(2).click();

          await expect(page1.locator('.winner-symbol')).toHaveText('O');
          await expect(page2.locator('.winner-symbol')).toHaveText('O');
          await expect(page1.locator('.result-info')).toHaveText('YOU WON!');
          await expect(page2.locator('.result-info')).toHaveText('YOU LOST!');
        });

        test('second player won', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page1.locator('.cell').nth(0).click();
          await page2.locator('.cell').nth(3).click();
          await page1.locator('.cell').nth(1).click();
          await page2.locator('.cell').nth(4).click();
          await page1.locator('.cell').nth(6).click();
          await page2.locator('.cell').nth(5).click();

          await expect(page1.locator('.winner-symbol')).toHaveText('X');
          await expect(page2.locator('.winner-symbol')).toHaveText('X');
          await expect(page1.locator('.result-info')).toHaveText('YOU LOST!');
          await expect(page2.locator('.result-info')).toHaveText('YOU WON!');
        });

        test('tie', async ({ context }) => {
          const [page1, page2] = context.pages();
  
          await page1.locator('.cell').nth(0).click();
          await page2.locator('.cell').nth(8).click();
          await page1.locator('.cell').nth(1).click();
          await page2.locator('.cell').nth(7).click();
          await page1.locator('.cell').nth(6).click();
          await page2.locator('.cell').nth(2).click();
          await page1.locator('.cell').nth(5).click();
          await page2.locator('.cell').nth(3).click();
          await page1.locator('.cell').nth(4).click();
  
          await expect(page1.locator('.winner-symbol')).toHaveText('O / X');
          await expect(page2.locator('.winner-symbol')).toHaveText('O / X');
          await expect(page1.locator('.result-info')).toHaveText('TIE!');
          await expect(page2.locator('.result-info')).toHaveText('TIE!');
        });
      });
      
      test.describe('Displaying playing again status', async () => {
        test.beforeEach(async ({ context }) => playTheGame(context));

        test('first player wants to play again', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page1.locator('.buttons button').first().click();

          await expect(page1.locator('.play-again-status').first()).toHaveText('\u2714');
          await expect(page2.locator('.play-again-status').first()).toHaveText('\u2714');
        });

        test('second player wants to play again', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page2.locator('.buttons button').first().click();

          await expect(page1.locator('.play-again-status').last()).toHaveText('\u2714');
          await expect(page2.locator('.play-again-status').last()).toHaveText('\u2714');
        });

        test('first player does not want to play again', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page1.locator('.buttons button').last().click();

          await expect(page2.locator('.play-again-status').first()).toHaveText('\u2717');
        });

        test('second player does not want to play again', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page2.locator('.buttons button').last().click();

          await expect(page1.locator('.play-again-status').last()).toHaveText('\u2717');
        });

        test('one player closes the page', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page1.close();

          await expect(page2.locator('.play-again-status').first()).toHaveText('\u2717');
        });

        test('one player goes back into the main page by url', async ({ context }) => {
          const [page1, page2] = context.pages();

          await page2.goto('/');

          await expect(page1.locator('.play-again-status').last()).toHaveText('\u2717');
        });
      });

      test.describe('Restarting the game', async () => {
        test.beforeEach(async ({ context }) => {
          await playTheGame(context);
          await restartTheGame(context);
        });

        // NOTE: The check if the game is NOT restarted when one or neither of the players wants to is not necessary,
        // as it is already checked in 'Displaying playing again status' section - if playing again status is shown, then the game is not restarted
        
        test('should restart the game when both players want to', async ({ context }) => {
          const [page1, page2] = context.pages();

          await expect(page1.locator('.overlay')).not.toBeVisible();
          await expect(page2.locator('.overlay')).not.toBeVisible();
        });
        
        test.describe('After the restart', async () => {
          test('should clear up the board', async ({ context }) => {
            const [page1, page2] = context.pages();
            
            for (const cell of await page1.locator('.cell').all()) {
              await expect(cell).toHaveText('');
            }
            for (const cell of await page2.locator('.cell').all()) {
              await expect(cell).toHaveText('');
            }
          });

          test('should clear up the message', async ({ context }) => {
            const [page1, page2] = context.pages();
            
            await expect(page1.locator('.message')).toHaveText('');
            await expect(page2.locator('.message')).toHaveText('');
          });

          test('should reverse the turn', async ({ context }) => {
            const [page1, page2] = context.pages();
            
            await page1.locator('.cell').nth(0).click();
            
            await expect(page1.locator('.message')).toHaveText(MESSAGES[1]);
            await expect(page2.locator('.cell').nth(0)).toHaveText('');

            await page2.locator('.cell').nth(0).click();
            await page1.locator('.cell').nth(1).click();

            await expect(page1.locator('.cell').nth(0)).toHaveText('O');
            await expect(page1.locator('.cell').nth(1)).toHaveText('X');
          });
        });
      });
    });
  });
});

const rejoin = async (page: Page) => {
  await page.goto('/');
  await page.locator('.room').first().click();
  await page.waitForTimeout(TIMEOUT);
} 