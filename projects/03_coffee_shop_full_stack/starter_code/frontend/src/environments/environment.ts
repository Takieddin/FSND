/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'ta9i.auth0.com', // the auth0 domain prefix
    audience: 'CoffeShopAPI', // the audience set for the auth0 app
    clientId: 'zKN4RyWbYpSeiCAI1aQZz994j3VP7Cdw', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
