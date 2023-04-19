/**
 * @jest-environment jsdom
 */

const {setTimeout} = require("../message");

it('should set alert to "close" after 2990ms', (done) => {
    setTimeout(() => {
        expect(alert.close);
        done();
      }, 2990);
    });